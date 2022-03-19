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


def _calculate_word_scores(max_freq, frequencies, wordlist):

    word_scores = {}

    for w in wordlist:
        word_scores[w] = 0
        for i in range(0, 5):
            word_scores[w] += max_freq[i] - frequencies[w[i]][i]

    return word_scores


# wrapper function, exposed function
def get_highest_frequency(game):
    wordlist = game.get_remaining_answers
    freq = _get_frequencies(wordlist)
    max_freq = _calculate_max_frequency(freq)
    scores = _calculate_word_scores(max_freq, freq, wordlist)

    return min(scores, key=scores.get)
