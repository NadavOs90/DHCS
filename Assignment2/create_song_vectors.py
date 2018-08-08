from math import log10
from random import uniform


def calc_avg_song_length(all_songs):
    avg = 0
    for song_index, song_name, song_words in all_songs:
        avg += len(song_words)
    avg /= len(all_songs)
    return avg


def create_song_vectors(all_word_vectors, all_words_indexs, all_songs, base_song):
    k1 = uniform(1.2, 2.0)
    b = 0.75
    avg_song_leangth = calc_avg_song_length(all_songs)
    song_vectors = [None] * len(all_songs)
    idf_vector = [0] * len(all_words_indexs)
    for word in all_words_indexs.iterkeys():
        count_songs_without_word = all_word_vectors[all_words_indexs[word]].count(0)
        df = len(all_word_vectors[all_words_indexs[word]]) - count_songs_without_word
        idf_vector[all_words_indexs[word]] = log10((len(all_songs) + 1) / df)
    for song_index, song_name, song_words in all_songs:
        tf_vector = [0] * len(all_words_indexs)
        flat_words = list(set(song_words))
        for word in flat_words:
            numerator = all_word_vectors[all_words_indexs[word]][song_index] * (k1 + 1)
            denominator = all_word_vectors[all_words_indexs[word]][song_index]
            denominator += k1 * (1 - b + b * (float(len(song_words)) / avg_song_leangth))
            tf_vector[all_words_indexs[word]] = numerator / denominator
        song_vectors[song_index] = tf_vector
        if song_name == base_song:
            base_song = tf_vector
    all_songs = map(lambda song: (song[0], song[1]), all_songs)
    return song_vectors, idf_vector, all_songs, base_song


