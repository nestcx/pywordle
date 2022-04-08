import string

def _get_frequencies(wordlist):

    frequencies = {}

    for letter in list(string.ascii_lowercase):
        frequencies[letter] = [0,0,0,0,0]

    for w in wordlist:
        for i in range(0,5):
            frequencies[w[i]][i] += 1

    return frequencies


def _calculate_max_frequency(frequencies):

    max_freq = [0,0,0,0,0]

    for l in frequencies:
        for i in range(0, 5):
            if frequencies[l][i] > max_freq[i]:
                max_freq[i] = frequencies[l][i]

    return max_freq


def _calculate_word_scores(max_freq, frequencies, wordlist, true_yellow):

    word_scores = {}

    for w in wordlist:
        word_scores[w] = 0
        for i in range(0, 5):
            word_scores[w] += max_freq[i] - frequencies[w[i]][i]

    return word_scores

def _calculate_word_scores2(max_freq, frequencies, wordlist, true_yellow):

    word_scores = {}

    for w in wordlist:
        word_scores[w] = 0
        for i in range(0, 5):
            word_scores[w] += max_freq[i] - frequencies[w[i]][i]
    return word_scores

def get_highest_frequency(wordlist, wordlist2, true_yellow, turn_no):
    freq = _get_frequencies(wordlist)
    max_freq = _calculate_max_frequency(freq)
    if turn_no == 2:
        scores = _calculate_word_scores(max_freq, freq, wordlist2, true_yellow)
    else:
        scores = _calculate_word_scores2(max_freq, freq, wordlist2, true_yellow)

    return min(scores, key=scores.get)
