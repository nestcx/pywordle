from pywordle.examples.maximise_similarity.cleanup_guess import cleanup
from pywordle.examples.maximise_similarity.word_frequency import get_highest_frequency
from pywordle.pywordle.pywordle import Wordle
import copy

def determine_best_guess(game):
    guess = ''

    if cleanup(game) != False:
        guess = cleanup(game)
    else:
       guess = get_highest_frequency(game.get_remaining_answers, game.get_remaining_answers, game.true_yellow, game.turn_no)
    return guess