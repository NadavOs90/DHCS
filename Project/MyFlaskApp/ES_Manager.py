from elasticsearch import Elasticsearch
import json
import subprocess
import sys
import requests
from Project.MyFlaskApp.validate import validate_song, validate_concert, validate_album


class ES_Manager(object):
    def __init__(self, band):
        try:
            res = requests.get('http://localhost:9200')
            if res.status_code != 200 and json.loads(res.content)['cluster_name'] != 'elasticsearch':
                self.create_es()
        except:
            self.create_es()
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.band = band

    @staticmethod
    def create_es():
        # es_bat_path = "C:\\Users\\nadav.ostrowsky\\Downloads\\elasticsearch-6.3.1\\bin\\elasticsearch"
        es_bat_path = raw_input('Enter Elasticsearch batch file path: ')
        p = subprocess.Popen(["powershell.exe", es_bat_path], stdout=sys.stdout)
        p.communicate()

    def del_item(self, index, idd):
        self.es.delete(index=index, doc_type=self.band, id=idd)

    def add(self, item, index):
        if index == 'Song' and validate_song(item):
            self.new_song(item)
        elif index == 'Concert' and validate_concert(item):
            self.new_concert(item)
        elif index == 'Album' and validate_album(item):
            self.new_album(item)
        else:
            return False
        return True

    def get_all_values_for_index(self, index):
        res = self.es.search(index=index, doc_type=self.band)['hits']['hits']
        if len(res) == 0:
            return []
        else:
            ans = []
            for hit in res:
                ans.append(hit['_source'])
            return ans

    def new_item(self, item, index, idd):
        if isinstance(item, dict):
            json_object = item
        else:
            print 'Error in new item'
            return False
        self.es.index(index=index, doc_type=self.band, body=json_object, id=idd)

    def new_song(self, song):
        if isinstance(song, str) or isinstance(song, unicode):
            song = json.loads(song)
        idd = song['song_title']
        self.new_item(song, 'song', idd)

    def new_album(self, album):
        if isinstance(album, str) or isinstance(album, unicode):
            album = json.loads(album)
        idd = album['album_name']
        self.new_item(album, 'album', idd)

    def new_concert(self, concert):
        if isinstance(concert, str) or isinstance(concert, unicode):
            concert = json.loads(concert)
        idd = concert['date'] + concert['location']
        self.new_item(concert, 'concert', idd)

    def del_song(self, song):
        if isinstance(song, str) or isinstance(song, unicode):
            song = json.loads(song)
        idd = song['song_title']
        self.del_item(index='song', idd=idd)

    def del_album(self, album):
        if isinstance(album, str) or isinstance(album, unicode):
            album = json.loads(album)
        idd = album['album_name']
        self.del_item(index='album', idd=idd)

    def del_concert(self, concert):
        if isinstance(concert, str) or isinstance(concert, unicode):
            concert = json.loads(concert)
        idd = concert['date'] + concert['location']
        self.del_item(index='concert', idd=idd)

    def search_prefix(self, string, index=None):
        query = {
            "query": {
                "multi_match": {
                    "query": string,
                    "type": "phrase_prefix",
                    "fields": []
                }
            }
        }
        res = self.es.search(doc_type=self.band, body=query, index=index)['hits']['hits']
        if len(res) == 0:
            return []
        else:
            ans = []
            for hit in res:
                ans.append(hit['_source'])
            return ans

    def search_song(self, song):
        res = self.search_prefix(song, 'song')
        ans = []
        for s in res:
            ans.append('Title: {}'.format(s['song_title']))
            ans.append('Album: {}'.format(s['album']))
            ans.append('Lyrics: ')
            for line in s['lyrics']:
                ans.append(line)
            ans.append('\n')
            ans.append('\n')
        return ans

    def search_album(self, album):
        res = self.search_prefix(album, 'album')
        ans = []
        for s in res:
            ans.append('Title: {}'.format(s['album_name']))
            ans.append('Release Year: {}'.format(s['release_year']))
            ans.append('Songs: ')
            for line in s['songs']:
                ans.append(line)
            ans.append('\n')
            ans.append('\n')
        return ans

    def search_concert(self, concert):
        res = self.search_prefix(concert, 'concert')
        ans = []
        for s in res:
            ans.append('Date: {}'.format(s['date']))
            ans.append('Location: {}'.format(s['location']))
            ans.append('Set List: ')
            for line in s['setlist']:
                ans.append(line)
            ans.append('\n')
            ans.append('\n')
        return ans

    def get_lyrics(self, song):
        res = self.search_prefix(song, 'song')
        songs = filter(lambda s: song.lower() in s['song_title'].lower(), res)
        for song in songs:
            lyrics = song['lyrics']
        return lyrics

    def get_locations(self, song):
        res = self.search_prefix(song, 'concert')
        concerts = [c['location'] for c in res if song.title() in c['setlist']]
        return concerts

    def get_album_distribution(self, year):
        res = self.search_prefix(year, 'concert')
        if len(res) == 0:
            return ['No concerts for the year {}'.format(year)]
        set_lists = map(lambda concert: concert['setlist'], res)
        flat_set_lists = [song.lower() for set_list in set_lists for song in set_list]
        albums = self.get_all_values_for_index('album')
        amount_of_songs_in_setlists = len(flat_set_lists)
        ans = []
        for album in albums:
            percentage = 0.0
            for song in album['songs']:
                percentage += flat_set_lists.count(song.lower())
            percentage /= amount_of_songs_in_setlists
            percentage *= 100
            s = '{} - was in {}% of the Concerts'.format(album['album_name'], round(percentage, 2))
            ans.append(s)
        return ans

    def get_song_stat(self, song):
        res = self.search_song(song)
        if len(res) == 0:
            return ["Couldn't find {}".format(song)]
        res = self.get_all_values_for_index('concert')
        set_lists = map(lambda concert: concert['setlist'], res)
        flat_set_lists = [s.lower() for set_list in set_lists for s in set_list]
        amount_of_concerts = len(res)
        stat = flat_set_lists.count(song.lower())*100.0 / amount_of_concerts
        stat = round(stat, 2)
        return ['{} has a {}% chance of appearing in the next concert'.format(song.title(), stat)]