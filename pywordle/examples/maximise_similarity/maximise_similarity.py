from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.solvetracker import SolveTracker
from cleanup_word import cleanup, cleanup
from word_frequency import get_highest_frequency
from alive_progress import alive_bar



def determine_best_guess(game):
    guess = ''
    
    if cleanup(game) != False:
        guess = cleanup(game)
    else:
        guess = get_highest_frequency(game)

    return guess



game_count = 2315
tracker = SolveTracker(turn_limit=6)

with alive_bar(game_count, stats=False) as bar:
    for i in range(0, game_count):

        game = Wordle(word_index=i)
        game.turn('salet')

        while game.state == "active":
            
            remaining_words = game.get_remaining_answers

            guess = determine_best_guess(game)
            
            turn = game.turn(guess)

            if game.state == "loss":
                print(game.word)

        tracker.submit(game)
        bar()

print()
print(f'average turns: {tracker.get_stats()["avg_turns"]}')
print(tracker.get_graph())