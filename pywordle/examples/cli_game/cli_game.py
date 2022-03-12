import os
from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.cli_keyboard import generate_coloured_keyboard
from pywordle.utils.cli_colour_string import *


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def guess_output(guess, colour_sequence):
    output = ""

    i = 0
    while i < 5:
        if colour_sequence[i] == 0:
            output = output + colour_string(BLACK, LIGHTGREY, guess[i])
        elif colour_sequence[i] == 1:
            output = output + colour_string(GREEN, BLACK, guess[i])
        elif colour_sequence[i] == 2:
            output = output + colour_string(YELLOW, BLACK, guess[i])
        i = i + 1
    
    return output


game = Wordle(turn_limit=10, word_index=1)

guesses = []
colour_sequences = []


def get_turn_history():
    output = ""
    
    i = 1
    while i <= game.turn_limit:

        g = f'{i}: '

        if i <= game.turn_no - 1:
            g += guess_output(guesses[i-1], colour_sequences[i-1])

        output += g + '\n'

        i += 1

    return output


def display_game_screen(message=""):
    clear_terminal()
    print(game.debug_info)
    print(get_turn_history())
    print(generate_coloured_keyboard(game.get_keyboard_data))
    rem = game.get_remaining_words
    if len(rem) < 50:
        print(game.get_remaining_words)
    print(message)


display_game_screen()


while game.state == "active":

    guess = input(f'{game.turn_no}: ')
    response = game.turn(guess)


    if response == False:
        display_game_screen("Invalid guess - Try again")
        continue
    else:
        guesses.append(response["guess"])
        colour_sequences.append(response["colour_sequence"])

        display_game_screen()



message = ""

if game.state == "win":
    message = "You Win!"
elif game.state == "loss":
    message = f'The word was: {game.word}'

display_game_screen(message)