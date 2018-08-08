

def create_word_vectors(all_songs):
    # word_count = 0
    word_count_list = [None] * len(all_songs)
    all_word_count_dict = {}
    for song_index, song_name, song_words in all_songs:
        word_count_dict = {word: song_words.count(word) for word in song_words}
        for word, count in word_count_dict.iteritems():
            # word_count += count
            if all_word_count_dict.get(word):
                all_word_count_dict[word] += count
            else:
                all_word_count_dict[word] = count
        word_count_list[song_index] = word_count_dict

    all_word_vectors = [None] * len(all_word_count_dict)
    all_word_vectors_index = 0
    all_words_indexs = {}
    for word, count in all_word_count_dict.iteritems():
        vector = [0] * len(all_songs)
        for index in xrange(len(all_songs)):
            try:
                vector[index] = word_count_list[index][word]
            except KeyError:
                pass
        all_word_vectors[all_word_vectors_index] = vector
        all_words_indexs[word] = all_word_vectors_index
        all_word_vectors_index += 1
    return all_word_vectors, all_words_indexs, all_songs
