from pywordle.pywordle.pywordle import Wordle
from maximise_similarity import determine_best_guess
import json

game = Wordle(gametype="select", answer="joker")

while game.state == "active":
    
    remaining_words = game.get_remaining_answers

    guess = determine_best_guess(game)
    
    turn = game.turn(guess)

    if game.state == "loss":
        print(game.answer)
    
    print(f'{game.turn_no}:  {guess} - {game.get_remaining_answers}')

    latest_turn = list(game.turn_history)[-1]
    cs = game.turn_history[latest_turn]["result"]
    print(f'green_count: {cs.count(1)}')

    print(f'true yellow: {game.true_yellow}')

    input()


print(json.dumps(game.turn_history, indent=4))