#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from BeautifulSoup import BeautifulSoup


def get_metadata(directory, song_names):
    res = []
    for filename in os.listdir(directory):
        try:
            sub_directory = unicode(directory + u'\\{}'.format(filename))
            for sub_filename in os.listdir(sub_directory):
                if sub_filename.endswith(".xml"):
                    split = sub_filename.split('.')[0]
                    if split in song_names:
                        with open(sub_directory+u'\\{}'.format(sub_filename)) as xml_file:
                            xml = BeautifulSoup(xml_file.read())
                            metadata = {
                                'title': xml.find('title').text,
                                'singer': xml.find('singer').text,
                                'writer': xml.find('writer').text,
                                'album': xml.find('album').text,
                                'date': xml.find('date').text,
                                'composer': xml.find('composer').text
                            }
                            res.append(metadata)
        except:
            pass
    for song in res:
        for k, v in song.iteritems():
            print k, ':', v
        print
