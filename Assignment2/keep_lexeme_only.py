#!/usr/bin/env python
# -- coding: utf-8 --
import os

def keep_lexeme_only(directory):
    for filename in os.listdir(directory):
        try:
            sub_directory = unicode(directory + u'\\{}'.format(filename))
            for sub_filename in os.listdir(sub_directory):
                if not sub_filename.startswith("new_"):
                    with open (sub_directory+'\\new_'+sub_filename,'w') as out:
                        with open(sub_directory+'\\'+sub_filename) as inp:
                            for line in inp:
                                nline=line.split(' ')
                                if len(nline)>2:
                                    if not nline[2] in stopwords:
                                        out.write(nline[2]+'\n')
                    os.remove(sub_directory+'\\'+sub_filename)

        except:
            pass