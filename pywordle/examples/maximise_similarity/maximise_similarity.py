from pywordle.examples.maximise_similarity.cleanup_word import cleanup
from pywordle.examples.maximise_similarity.word_frequency import get_highest_frequency

def determine_best_guess(game):
    guess = ''

    if len(game.get_remaining_answers) <= 2:
        guess = game.get_remaining_answers[0]
    elif cleanup(game) != False:
        guess = cleanup(game)
    else:
        guess = get_highest_frequency(game)

    return guess