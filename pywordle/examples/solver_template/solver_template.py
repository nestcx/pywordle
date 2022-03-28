from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.solvetracker import SolveTracker
from alive_progress import alive_bar
import random

def determine_best_guess(game):
    return random.choice(game.get_remaining_answers)


game_count = len(Wordle().valid_answer_list)
tracker = SolveTracker(turn_limit=6)

with alive_bar(game_count) as bar:
    for i in range(0, game_count):

        game = Wordle(word_index=i)

        while game.state == "active":
            guess = determine_best_guess(game)
            game.turn(guess)

            if game.state == "loss":
                print(game.answer)

        tracker.submit(game)
        bar()

print(tracker.get_stats())