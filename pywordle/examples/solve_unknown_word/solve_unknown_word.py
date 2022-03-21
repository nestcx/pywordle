from pywordle.pywordle.pywordle import Wordle
from alive_progress import alive_bar


game = Wordle(gametype="unknown")

def find_best(game):
    gamestate = game.gamestate
    remaining_answers = game.get_remaining_answers
    guess_list = Wordle.valid_guess_list
    scores = {}


    for guess in guess_list:
        scores[guess] = 0

    with alive_bar(2, stats=False) as bar:

        for answer in remaining_answers:            
            print(answer)

            for i in range(2):
                mgame = Wordle(gamestate=gamestate)
                mgame.word = answer
                mgame.turn(guess_list[i])
                print(guess_list[i])
                scores[guess] += len(mgame.get_remaining_answers)
                print(f'Helloooo {len(mgame.get_remaining_answers)} ')

            bar()

    return scores


while True:

    guess = input(f"Guess {game.turn_no}: ")
    cs_input = input(f"Colour sequence {game.turn_no}: ")
    colour_sequence = list(map(int, cs_input))

    result = game.turn(guess, colour_sequence)

    if result == False:
        print("invalid guess!")
        continue

    find_best(game)

    print(result)
    print(game.get_remaining_answers)
