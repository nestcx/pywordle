from pywordle.pywordle.pywordle import Wordle
from alive_progress import alive_bar
import copy


def determine_best_guess(gamestate):

    game = Wordle(gamestate=gamestate)

    remaining_answers = game.get_remaining_answers
    guess_list = game.valid_guess_list

    guess_scores = {}

    for guess in guess_list:
        guess_scores[guess] = 0


    with alive_bar(len(guess_list)) as bar:

        for guess in guess_list:

            for answer in remaining_answers:
                
                g = copy.deepcopy(gamestate)
                game = Wordle(gamestate=g)

                game.word = answer

                game.turn(guess)
                
                rem_count = len(game.get_remaining_answers)
                guess_scores[guess] += rem_count
            
            bar()
        
    return guess_scores



game_count = 1

for i in range(0, game_count):

    game = Wordle(gametype="select", word="mangy")
    game.turn("pinky")
    print(f'rem: {len(game.get_remaining_answers)}')

    gamestate = (game.gamestate)

    guess_scores = determine_best_guess(gamestate)

    sorted_dict = {}
    
    sorted_keys = sorted(guess_scores, key=guess_scores.get)

    for w in sorted_keys:
        sorted_dict[w] = guess_scores[w]

    print(sorted_dict)