from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.solvetracker import SolveTracker
from alive_progress import alive_bar
import string
import random


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



game_count = 2315
tracker = SolveTracker()

with alive_bar(game_count, stats=False) as bar:
    for i in range(0, game_count):

        game = Wordle(word_index=i)
        game.turn('salet')

        while game.state == "active":

            freq = get_frequencies(game.get_remaining_answers)
            max_freq = calculate_max_frequency(freq)
            scores = calculate_word_scores(max_freq, freq, game.get_remaining_answers)
            guess = determine_best_guess(scores, game.turn_no)
            guess = random.choice(game.get_remaining_answers)
            turn = game.turn(guess)
            #print(f'{guess} - {turn["colour_sequence"]} - {scores[guess]}')

            if game.state == "loss":
                print(game.word)

        tracker.submit(game)
        bar()

print(tracker.get_stats())