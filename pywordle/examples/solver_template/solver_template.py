from pywordle import MY_WORD_LIST
from pywordle.utils.clear_terminal import clear_terminal
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

        game = Wordle(answer_index=i, valid_answer_list = MY_WORD_LIST)

        while game.state == "active":
            guess = determine_best_guess(game)
            game.turn(guess)

            if game.state == "loss":
                print(game.answer)

        tracker.submit(game)
        clear_terminal()
        print(tracker.get_graph())
        
        bar()

print(tracker.get_stats())