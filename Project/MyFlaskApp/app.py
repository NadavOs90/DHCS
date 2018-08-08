from flask import Flask, render_template, request
from ES_Manager import ES_Manager
from wtforms import Form, StringField, TextAreaField, validators, SelectField, DateField, RadioField
from Project.MyFlaskApp.validate import validate_date, validate_location

app = Flask(__name__)
app.debug = True
esm = ES_Manager('a7x')


class Download(Form):
    index = RadioField('Select Index', choices=[('album', 'Albums'), ('concert', 'Concert'), ('song', 'Songs')])


class Discography(Form):
    choices = esm.get_all_values_for_index('album')
    choices = map(lambda a: (a['album_name'], a['album_name']), choices)
    album = RadioField('Albums', choices=choices)


class Search(Form):
    song_search = StringField('Search for Song Data: ', [validators.Length(min=1)])
    album_search = StringField('Search for Album Data: ', [validators.Length(min=1)])
    concert_search = StringField('Search for Concert Data: ', [validators.Length(min=1)])
    search_lyrics = StringField('Search for Song Lyrics: ', [validators.Length(min=1)])
    search_locations = StringField('Search for Concerts that played a Song: ', [validators.Length(min=1)])


class AddJson(Form):
    json_string = TextAreaField('Enter Song/Album/Concert JSON')
    index = SelectField('Select what Data you would like to add')


class AlbumDistribution(Form):
    year = DateField('Enter the Year:   ', format='%Y')


class SongStat(Form):
    song = StringField('Enter Song Name:  ', [validators.Length(min=1)])


class Band(Form):
    band_name = StringField('Enter Band Name:  ', [validators.Length(min=1)])


class Song(Form):
    song_title = StringField('Enter Song Name:  ', [validators.Length(min=1)])
    album = StringField('Enter Album Name:  ', [validators.Length(min=1)])
    lyrics = TextAreaField('Enter Song Lyrics:  ')


class Concert(Form):
    date = StringField('Enter Concert Date (JUN 22 2018):  ', [validators.Length(min=1)])
    location = StringField('Enter Concert Location (Boeretang, Dessel, Belgium):  ', [validators.Length(min=1)])
    setlist = TextAreaField('Enter Set List:  ')


class Album(Form):
    album_name = StringField('Enter Album Name:  ', [validators.Length(min=1)])
    release_year = DateField('Enter Release Year:   ', format='%Y')
    songs = TextAreaField('Enter Song List:  ')


@app.route('/', methods=['GET', 'POST'])
def hello():
    form = Band(request.form)
    if request.method == 'POST':
        band_name = form.band_name.data
        global esm
        esm = ES_Manager(band_name)
    return render_template('home.html', form=form)


@app.route('/add_concert', methods=['GET', 'POST'])
def add_concert():
    form = Concert(request.form)
    if request.method == 'POST':
        date = form.date.data
        location = form.location.data
        if not validate_date(date) or not validate_location(location):
            return render_template('fail.html', index='Concert')
        setlist = form.setlist.data
        setlist = setlist.split('\n')
        new_concert = {
            'date': date,
            'location': location,
            'setlist': setlist
        }
        esm.new_concert(new_concert)
        return render_template('success.html', index='Concert')
    return render_template('add_concert.html', form=form)


@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    form = Song(request.form)
    if request.method == 'POST':
        song_title = form.song_title.data
        album = form.album.data
        lyrics = form.lyrics.data
        lyrics = lyrics.split('\n')
        new_song = {
            'song_title': song_title,
            'album': album,
            'lyrics': lyrics
        }
        esm.new_song(new_song)
        return render_template('success.html', index='Song')
    return render_template('add_song.html', form=form)


@app.route('/add_album', methods=['GET', 'POST'])
def add_album():
    form = Album(request.form)
    if request.method == 'POST':
        album_name = form.album_name.data
        release_year = form.release_year.data
        songs = form.songs.data
        songs = songs.split('\n')
        new_album = {
            'album_name': album_name,
            'release_year': release_year,
            'lyrics': songs
        }
        esm.new_album(new_album)
        return render_template('success.html', index='Album')
    return render_template('add_album.html', form=form)


@app.route('/add', methods=['GET', 'POST'])
def add():
    indexes = ['Song', 'Album', 'Concert']
    form = AddJson(request.form)
    if request.method == 'POST':
        json_string = form.json_string.data
        index = form.index.data
        res = esm.add(json_string, index)
        if res:
            return render_template('success.html', index=index)
        return render_template('fail.html', index=index)
    return render_template('add.html', form=form, indexes=indexes)


@app.route('/album_distribution', methods=['POST', 'GET'])
def album_success():
    form = AlbumDistribution(request.form)
    res = []
    if request.method == 'POST':
        year = form.year.data.year
        res = esm.get_album_distribution(year)
    return render_template('album_distribution.html', form=form, results=res)


@app.route('/song_stat', methods=['POST', 'GET'])
def song_stat():
    form = SongStat(request.form)
    res = []
    if request.method == 'POST':
        song = form.song.data
        res = esm.get_song_stat(song)
    return render_template('song_stat.html', form=form, results=res)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = Search(request.form)
    if request.method == 'POST':
        song_search = form.song_search.data
        album_search = form.album_search.data
        concert_search = form.concert_search.data
        search_lyrics = form.search_lyrics.data
        search_locations = form.search_locations.data
        res = 'Not Found'
        if song_search:
            res = esm.search_song(song_search)
        elif album_search:
            res = esm.search_album(album_search)
        elif concert_search:
            res = esm.search_concert(concert_search)
        elif search_lyrics:
            res = esm.get_lyrics(search_lyrics)
        elif search_locations:
            res = esm.get_locations(search_locations)
        return render_template('search.html', form=form, results=res)
    return render_template('search.html', form=form)


@app.route('/discography', methods=['GET', 'POST'])
def discography():
    form = Discography(request.form)
    res = []
    if request.method == 'POST':
        album = form.album.data
        res = esm.search_prefix(album, 'album')
        if len(res) > 0:
            res = res[0]['songs']
    return render_template('discography.html', form=form, results=res)


@app.route('/download', methods=['GET', 'POST'])
def download():
    form = Download(request.form)
    res = []
    if request.method == 'POST':
        index = form.index.data
        res = esm.get_all_values_for_index(index)
    return render_template('download.html', form=form, results=res)


if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0')
