from pywordle.examples.maximise_similarity.cleanup_guess import cleanup
from pywordle.examples.maximise_similarity.word_frequency import get_highest_frequency
from pywordle.pywordle.pywordle import Wordle
import copy

def determine_best_guess(game):
    guess = ''

    if cleanup(game) != False:
        guess = cleanup(game)
    else:
        if game.turn_no == 2:
        #    guess = get_highest_frequency(game.get_remaining_answers, game.valid_guess_list)
            gamestate = game.gamestate
            lowest_rem = 999
            guess = ''
            for vg in game.valid_guess_list:
                g = Wordle(gamestate=gamestate)
                rem = copy.deepcopy(g.get_remaining_answers)
                g.turn(vg)
                if len(rem) < lowest_rem:
                    lowest_rem = len(rem)
                    guess = vg
        else:
            guess = get_highest_frequency(game.get_remaining_answers, game.get_remaining_answers)

    return guess