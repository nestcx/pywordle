from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.solvetracker import SolveTracker
from alive_progress import alive_bar
import random

def determine_best_guess(guess_list, answer_list, remaining_words):
    return random.choice(remaining_words)


game_count = len(Wordle().valid_answer_list)
tracker = SolveTracker()

with alive_bar(game_count, stats=False) as bar:
    for i in range(0, game_count):

        game = Wordle(word_index=i)
        game.turn('slate')

        while game.state == "active":
            guess = determine_best_guess(Wordle.valid_guess_list, Wordle.valid_answer_list, game.get_remaining_answers)
            game.turn(guess)

            if game.state == "loss":
                print(game.word)

        tracker.submit(game)
        bar()

print(tracker.get_stats())