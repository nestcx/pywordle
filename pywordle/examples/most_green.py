from py import process
from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.solvetracker import SolveTracker
from alive_progress import alive_bar
import random
import json

def process_guess(word, guess):

        colour_sequence = [0,0,0,0,0]

        coloured_letters = []
        yellow = []

        position_skip = []
        word_index_skip = []

      
        # direct matches
        i = 0
        while i < 5:
            if guess[i] == word[i]:
                position_skip.append(i)
                colour_sequence[i] = 1

                # add to coloured letters
                coloured_letters.append(guess[i])

            i = i + 1

        # indirect matches
        i = 0
        while i < 5:

            if i in position_skip:
                i = i + 1
                continue

            j = 0
            while j < 5:

                if j in position_skip or j in word_index_skip:
                    j = j + 1
                    continue

                if guess[i] == word[j]:
                    colour_sequence[i] = 2
                    word_index_skip.append(j)

                    # add to coloured letters
                    coloured_letters.append(guess[i])
                    
                    # add to yellow letters
                    yellow.append(guess[i])

                    break

                j = j + 1

            i = i + 1

        return colour_sequence


def get_avg(guess_list, answer_list, remaining_words):
    return random.choice(remaining_words)


game_count = len(Wordle().valid_answer_list)
tracker = SolveTracker()

f = open("c_avg.txt", 'w')
f2 = open("g_avg.txt", 'w')
f3 = open("y_avg.txt", 'w')

c_avg_dict = {}
g_avg_dict = {}
y_avg_dict = {}

def get_colour_counts(turn):
    results = {}
    results["c"] = turn.count(2) + turn.count(1)
    results["g"] = turn.count(1)
    results["y"] = turn.count(2)

    return results

def record_avg(word, avg, dict):
    dict[word] = sum(avg) / len(avg)
    #print(dict)

wl = Wordle().valid_answer_list

with alive_bar(game_count) as bar:

    # loop 1 - want avg colours return by running every word against every word once.
    for i in range(0, game_count):

        print(i)

        game = Wordle(word_index=i)

        avg_green = []
        avg_yellow = []
        avg_colour = []
        word = game.valid_answer_list[i]

        rem = game.get_remaining_answers

        for x in range(0, len(rem)):
            
            guess = rem[x]
            colours = game.turn(guess)["colour_sequence"]

            c = get_colour_counts(colours)
            avg_colour.append(c["c"])
            avg_green.append(c["g"])
            avg_yellow.append(c["y"])
        
        record_avg(word, avg_colour, c_avg_dict)
        record_avg(word, avg_green, g_avg_dict)
        record_avg(word, avg_yellow, y_avg_dict)
    
        bar()

f.write(json.dumps(c_avg_dict))
f2.write(json.dumps(g_avg_dict))
f3.write(json.dumps(y_avg_dict))

#print(t_avg_dict)
#f.close()