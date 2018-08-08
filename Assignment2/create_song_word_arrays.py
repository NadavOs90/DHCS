#!/usr/bin/env python
# -- coding: utf-8 --
import os


def create_song_word_arrays(directory):
    index=0
    res=[]
    with open (directory+'\\result.txt','w') as out:
        for filename in os.listdir(directory):
            try:
                sub_directory = unicode(directory + u'\\{}'.format(filename))
                for sub_filename in os.listdir(sub_directory):
                    vec=[index,sub_filename.replace(".txt",'').replace('new_new_',''),[]]
                    with open(sub_directory+'\\'+sub_filename) as inp:
                        for line in inp:
                            if line.replace('\n','')=='':
                                pass
                            else:
                                vec[2].append(line.replace('\n',''))
                    res.append(vec)
                    index+=1
            except:
                pass
        out.write(str(res)+'\n')
