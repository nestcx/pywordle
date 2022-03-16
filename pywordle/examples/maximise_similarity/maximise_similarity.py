from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.solvetracker import SolveTracker
from alive_progress import alive_bar
import string
import random
from collections import Counter


def get_frequencies(words):

    frequencies = {}

    for letter in list(string.ascii_lowercase):
        frequencies[letter] = [0,0,0,0,0]

    for w in words:
        for i in range(0,5):
            frequencies[w[i]][i] += 1

    return frequencies


def calculate_max_frequency(frequencies):

    max_freq = [0,0,0,0,0]

    for l in frequencies:
        for i in range(0, 5):
            if frequencies[l][i] > max_freq[i]:
                max_freq[i] = frequencies[l][i]

    return max_freq


def calculate_word_scores(max_freq, frequencies, remaining_words):

    word_scores = {}

    for w in remaining_words:
        word_scores[w] = 0
        for i in range(0, 5):
            word_scores[w] += max_freq[i] - frequencies[w[i]][i]

    return word_scores


def determine_best_guess(wordscores, turn):

    return min(wordscores, key=wordscores.get)



## CLEANUP WORD 
def get_rm_freq(remaining_words):
    return Counter(''.join(remaining_words))


def get_dm_freq(direct_matches):
    dm_freq = {}
    for m in direct_matches:
        dm_freq[m] = len(direct_matches[m])
    return dm_freq

def elim_m(remaining_words, dm_freq, rm_freq):
    letters = set(''.join(remaining_words))
    rem = []
    for l in letters:
        if l not in dm_freq:
            rem.append(l)
        else:
            if rm_freq[l] != dm_freq[l] * len(remaining_words):
                rem.append(l)
    
    return rem

def find_intersections(wordlist, letters):
    d = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
    for w in wordlist:
        x = len(letters.intersection(w))
        d[x].append(w)
    return d


def get_cleanup_word(all_words, remaining_words, direct_matches):
    rm_freq = get_rm_freq(remaining_words)
    dm_freq = get_dm_freq(direct_matches)
    rem = elim_m(remaining_words, dm_freq, rm_freq)
    ints = find_intersections(all_words, set(rem))

    word = ''
    for i in range(5, 0, -1):
        if ints[i] != []:
            word = ints[i][0]
            break
    
    return word

def get_green_count(direct_matches):
    c = 0
    for d in direct_matches:
        c += len(direct_matches[d])

    return c


game_count = 2315
tracker = SolveTracker(turn_limit=6)

with alive_bar(game_count, stats=False) as bar:
    for i in range(0, game_count):

        game = Wordle(word_index=i)
        game.turn('salet')

        while game.state == "active":
            
            remaining_words = game.get_remaining_answers

            freq = get_frequencies(remaining_words)
            max_freq = calculate_max_frequency(freq)
            scores = calculate_word_scores(max_freq, freq, remaining_words)

            # see if cleanup word is needed
            if get_green_count(game.direct_matches) >= 3 and get_green_count(game.direct_matches) < 5 and game.turn_no < 5:
                guess = get_cleanup_word(game.valid_answer_list + game.valid_guess_list, remaining_words, game.direct_matches)
            else:
                guess = determine_best_guess(scores, game.turn_no)
            
            turn = game.turn(guess)

            if game.state == "loss":
                print(game.word)

        tracker.submit(game)
        bar()

print()
print(tracker.get_graph())