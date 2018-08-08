#!/usr/bin/env python
# -- coding: utf-8 --
from Assignment2.create_song_word_arrays import create_song_word_arrays
from Assignment2.get_metadata import get_metadata
from Assignment2.keep_lexeme_only import keep_lexeme_only
from Assignment2.similarity import top10_similarity
from Assignment2.remove_stop_words import remove_stop_words
from Assignment2.unite_songs import unite_songs
from create_word_vectors import create_word_vectors
from create_song_vectors import create_song_vectors
import sys
from ast import literal_eval
import gc
import sys


def func(song):
    global counter
    counter += 1
    return counter, song[1], song[2]


if __name__ == '__main__':
    tagged_dir = unicode(sys.argv[1])
    xml_dir = unicode(sys.argv[2])
    base_song = raw_input('Enter Song Name: ').decode(sys.stdin.encoding)
    print 'Uniting Lyrics with Chorus'
    unite_songs(tagged_dir)
    print 'Getting Lexemes'
    keep_lexeme_only(tagged_dir)
    print 'Removing Stop Words'
    remove_stop_words(tagged_dir)
    print 'Creating Song Arrays'
    create_song_word_arrays(tagged_dir)
    gc.collect()
    all_songs = []
    counter = -1
    with open(tagged_dir + '\\result.txt', 'r') as input_file:
        for line in input_file:
            all_songs = literal_eval(line)
    all_songs = filter(lambda s: len(s[2]) > 0, all_songs)
    # all_songs = all_songs[:1000]
    all_songs = map(lambda s: func(s), all_songs)
    gc.collect()
    print 'Creating Vectors for each Word'
    all_word_vectors, all_words_indexs, all_songs = create_word_vectors(all_songs)
    gc.collect()
    print 'Creating Vectors for each Song'
    # base_song = u'נדליק ביחד נר'
    song_vectors, idf_vector, all_songs, base_song = create_song_vectors(all_word_vectors, all_words_indexs, all_songs, base_song)
    gc.collect()
    print 'Getting top 10 Similarities'
    top10_indexes = top10_similarity(song_vectors, idf_vector, base_song)
    gc.collect()
    top10_songs = []
    for song_index, song_name in all_songs:
        if song_index in top10_indexes:
            top10_songs.append(song_name)
            top10_indexes.remove(song_index)
    print 'The Top 10 Similar songs metadata are:'
    get_metadata(xml_dir, top10_songs)
