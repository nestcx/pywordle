from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.solvetracker import SolveTracker
from alive_progress import alive_bar

def determine_best_guess(wordlist, remaining_words):
    return "hello"


game_count = 100
tracker = SolveTracker()

with alive_bar(game_count, stats=False) as bar:
    for i in range(0, game_count):

        game = Wordle()

        while game.state == "active":
            guess = determine_best_guess(Wordle.wordlist, game.get_remaining_words)
            game.turn(guess)

        tracker.submit(game)
        bar()

print(tracker.get_stats())