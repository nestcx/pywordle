from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.cli_keyboard import generate_coloured_keyboard
from pywordle.utils.cli_colour_string import *
from pywordle.utils.clear_terminal import clear_terminal



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


def get_turn_history(game):
    output = ""
    th = game.turn_history
    i = 1
    while i <= game.turn_limit:
        output += f'{i}: '
        if game.turn_no > i:
            output += guess_output(th[i]["guess"], th[i]["result"])
        output += '\n'
        i += 1

    return output


def prettify_gamestate(game):
    output = ""
    gamestate = game.gamestate
    output += f'Gametype: {gamestate["gametype"]}' + '\n'
    output += f'Answer: {gamestate["answer"]}' + '\n'
    output += f'Turn No: {gamestate["turn_no"]}' + '\n'
    output += f'Turn Limit: {gamestate["turn_limit"]}' + '\n'
    output += f'State: {gamestate["state"]}' + '\n'
    output += f'Direct Matches: {gamestate["direct_matches"]}' + '\n'
    output += f'Indirect Matches: {gamestate["indirect_matches"]}' + '\n'
    output += f'Potential Frequency: {gamestate["potential_frequency"]}' + '\n'
    output += f'Definitive Frequency: {gamestate["definitive_frequency"]}' + '\n'
    output += f'Blacklist: {gamestate["blacklist"]}' + '\n'
    output += f'Remaining Words: {len(game.get_remaining_answers)}' + '\n'
    return output


def display_game_screen(game, message=""):

    clear_terminal()

    print(prettify_gamestate(game))
    print(get_turn_history(game))
    print(generate_coloured_keyboard(game.get_keyboard_data))

    rem = game.get_remaining_answers
    if len(rem) < 50:
        print(rem)

    print(message)



game = Wordle(turn_limit=10, gametype="select", answer="never")

display_game_screen(game)

while game.state == "active":

    guess = input(f'{game.turn_no}: ')

    response = game.turn(guess)

    if response == False:
        display_game_screen(game, message="Invalid guess - Try again")
        continue

    display_game_screen(game)


message = ""

if game.state == "win":
    message = "You Win!"
elif game.state == "loss":
    message = f'The answer was: {game.answer}'

display_game_screen(game, message)