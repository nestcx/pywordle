from pywordle.pywordle.pywordle import Wordle
from pywordle.examples.maximise_similarity.maximise_similarity import determine_best_guess
from pywordle.examples.maximise_similarity.cleanup_word import cleanup


game = Wordle(gametype="unknown")


while True:

    recommended = determine_best_guess(game)
    print(f'recommended guess: {recommended}')

    guess = input(f"Guess {game.turn_no}: ")
    cs_input = input(f"Colour sequence {game.turn_no}: ")
    colour_sequence = list(map(int, cs_input))
    
    result = game.turn(guess, colour_sequence)

    if result == False:
        print("invalid guess!")
        continue

    print(result)
    print(game.get_remaining_answers)
