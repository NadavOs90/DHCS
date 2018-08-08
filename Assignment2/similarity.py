from heapq import nlargest


def sim(song1_vector, song2_vector, idf_vector):
    ans = 0.0
    for word_index in range(len(song1_vector)):
        try:
            ans += song1_vector[word_index] * song2_vector[word_index] * idf_vector[word_index]
        except TypeError as e:
            pass
    return ans


def top10_similarity(song_vectors, idf_vector, base_song):
    top10 = []
    for i in range(len(song_vectors)):
        if song_vectors[i] != base_song:
            sim_res = sim(song_vectors[i], base_song, idf_vector)
            top10.append((sim_res, i))
            top10 = nlargest(10, top10)
    top10 = map(lambda x: x[1], top10)
    # top10 = list(sum(top10, ()))
    # top10 = list(set(top10))
    return top10
