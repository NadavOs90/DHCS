#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


directory = u'C:\\Users\\nadav.ostrowsky\\PycharmProjects\\DHCS\\Assignment2\\Lyrics\\Lyrics'
for filename in os.listdir(directory):
    try:
        sub_directory = unicode(directory + u'\\{}'.format(filename))
        for sub_filename in os.listdir(sub_directory):
            if sub_filename.endswith(".xml"):
                print sub_filename
            else:
                continue
    except:
        pass

