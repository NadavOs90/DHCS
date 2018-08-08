#!/usr/bin/env python
# -- coding: utf-8 --
import os


def unite_songs(directory):
    for filename in os.listdir(directory):
        try:
            sub_directory = unicode(directory + u'\\{}'.format(filename))
            # with open (sub_directory+"\\merge.txt",'w') as out:
            for sub_filename in os.listdir(sub_directory):
                if sub_filename.endswith("_Lyrics.txt"):
                    tmp='a'
                else:
                    tmp='w'
                newName = sub_filename.replace("_Lyrics","").replace("_Chorus","")
                with open (sub_directory+'\\'+newName,tmp) as out:
                    with open(sub_directory+'\\'+sub_filename) as inp:
                        for line in inp:
                            out.write(line)
                os.remove(sub_directory+'\\'+sub_filename)

        except:
            pass