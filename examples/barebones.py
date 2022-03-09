from pywordle.pywordle import Wordle

def determine_best_guess(wordlist, remaining_words):
    return "hello"


game_count = 100

for i in range(0, game_count):

    game = Wordle()

    while game.state == "active":
        guess = determine_best_guess(Wordle.wordlist, game.wordlist)
        game.turn(guess)