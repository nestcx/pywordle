import os
from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.cli_keyboard import generate_coloured_keyboard
from pywordle.utils.cli_colour_string import *
from collections import Counter


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


game = Wordle(turn_limit=10, word="saute")

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
    rem = game.get_remaining_answers
    if len(rem) < 50:
        print(rem)
    print(message)


## CLEANUP WORD 
def get_rm_freq(remaining_words):
    return Counter(''.join(remaining_words))


def get_dm_freq(direct_matches):
    dm_freq = {}
    for m in direct_matches:
        dm_freq[m] = len(direct_matches[m])
    return dm_freq

def elim_m(remaining_words, dm_freq, rm_freq):
    letters = set(''.join(remaining_words))
    rem = []
    for l in letters:
        if l not in dm_freq:
            rem.append(l)
        else:
            if rm_freq[l] != dm_freq[l] * len(remaining_words):
                rem.append(l)
    
    return rem

def find_intersections(wordlist, letters):
    d = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
    for w in wordlist:
        x = len(letters.intersection(w))
        d[x].append(w)
    return d


def get_cleanup_word(all_words, remaining_words, direct_matches):
    rm_freq = get_rm_freq(remaining_words)
    dm_freq = get_dm_freq(direct_matches)
    rem = elim_m(remaining_words, dm_freq, rm_freq)
    ints = find_intersections(all_words, set(rem))

    word = ''
    for i in range(5, 0, -1):
        if ints[i] != []:
            word = ints[i][0]
            break
    
    return word



display_game_screen()


while game.state == "active":

    guess = input(f'{game.turn_no}: ')
    if guess == 'cleanup':
        print(f'cleanup:  {get_cleanup_word(game.valid_guess_list + game.valid_answer_list, game.get_remaining_answers, game.return_all_data["direct_matches"])}')
        continue

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