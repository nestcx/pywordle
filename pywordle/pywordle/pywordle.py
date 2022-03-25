import random
from collections import Counter
from tkinter import N
from pywordle.helpers.elimination import eliminate_words
from pywordle.pywordle import DEFAULT_ANSWER_LIST, DEFAULT_GUESS_LIST

class Wordle():

    def __init__(self, gamestate = None, gametype = 'random', word = None, word_index = None, turn_limit = 6, valid_guess_list=DEFAULT_GUESS_LIST, valid_answer_list=DEFAULT_ANSWER_LIST):

        self.valid_guess_list = self.__read_wordlist(valid_guess_list)
        self.valid_answer_list = self.__read_wordlist(valid_answer_list)
        
        self.gametype = None
        self.word = None
        self.turn_no = None
        self.turn_limit = None
        self.turn_history = {}
        self.state = None
        self.direct_matches = {}
        self.indirect_matches = {}
        self.potential_frequency = {}
        self.definitive_frequency = {}
        self.blacklist = []

        if gamestate != None:
            self.__load_gamestate(gamestate)
        else:
            self.gametype = gametype
            if self.gametype == 'random':
                self.word = self.__get_random_word()
            elif self.gametype == 'unknown':
                self.word = None
            elif self.gametype == 'select':
                self.word = word
            elif self.gametype == 'index':
                self.word = self.valid_answer_list[word_index]

            self.state = "active"
            self.turn_no = 1
            self.turn_limit = turn_limit


    # getters

    @property
    def get_remaining_answers(self):
        data = {}
        data["direct_matches"] = self.direct_matches
        data["indirect_matches"] = self.indirect_matches
        data["potential_frequency"] = self.potential_frequency
        data["definitive_frequency"] = self.definitive_frequency
        data["blacklist"] = self.blacklist

        return eliminate_words(data, self.valid_answer_list)

    @property
    def get_keyboard_data(self):
        key_data = {}
        key_data["green"] = set(self.direct_matches.keys())
        key_data["yellow"] = set(self.indirect_matches) - key_data["green"]
        key_data["black"] = self.blacklist
        return key_data

    @property
    def get_keystrokes(self):
        return set.union(
            set(self.blacklist), 
            set(self.direct_matches), 
            set(self.indirect_matches))

    @property
    def gamestate(self):
        gamestate = {}
        gamestate["gametype"] = self.gametype
        gamestate["word"] = self.word
        gamestate["turn_no"] = self.turn_no
        gamestate["turn_limit"] = self.turn_limit
        gamestate["state"] = self.state
        gamestate["direct_matches"] = self.direct_matches
        gamestate["indirect_matches"] = self.indirect_matches
        gamestate["potential_frequency"] = self.potential_frequency
        gamestate["definitive_frequency"] = self.definitive_frequency
        gamestate["blacklist"] = self.blacklist

        return gamestate


    # private functions

    def __load_gamestate(self, gamestate):
        self.gametype = gamestate["gametype"]
        self.word = gamestate["word"]
        self.turn_no = gamestate["turn_no"]
        self.turn_limit = gamestate["turn_limit"]
        self.state = gamestate["state"]
        self.direct_matches = gamestate["direct_matches"]
        self.indirect_matches = gamestate["indirect_matches"]
        self.potential_frequency = gamestate["potential_frequency"]
        self.definitive_frequency = gamestate["definitive_frequency"]
        self.blacklist = gamestate["blacklist"]


    def __read_wordlist(self, wordlist):
        f = open(wordlist, 'r')
        wordlist = f.read().splitlines()
        f.close()
        return wordlist
        

    def __get_random_word(self):
        return(random.choice(self.valid_answer_list))

    
    # record direct and indirect matches dictionary
    def __record_letter_match(self, dict, letter, index):
        if letter not in dict:
            dict[letter] = []
    
        if index not in dict[letter]:
            dict[letter].append(index)

    def __record_potential_frequency(self, dict, letters):
        for x, i in letters.items():
            if (dict.get(x) == None or dict[x] < i):
                dict[x] = i
            
    def __record_blacklist(self, guess, coloured_letters):
        i = 0
        while i < 5:
            if guess[i] not in coloured_letters and guess[i] not in self.blacklist:
                self.blacklist.append(guess[i])
            i = i + 1


    def __process_guess(self, guess, colour_sequence=None):

        if colour_sequence == None:
            colour_sequence = [0,0,0,0,0]

        coloured_letters = []
        yellow = []

        position_skip = []
        word_index_skip = []

        # exact match
        if guess == self.word:
            self.state = "win"

        # direct matches
        i = 0
        while i < 5:
            if (self.gametype != 'unknown' and guess[i] == self.word[i]) or colour_sequence[i] == 1:
                colour_sequence[i] = 1
                position_skip.append(i)

                # record direct_match
                self.__record_letter_match(self.direct_matches, guess[i], i)

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

                if (self.gametype != 'unknown' and guess[i] == self.word[j]) or colour_sequence[i] == 2:
                    colour_sequence[i] = 2
                    word_index_skip.append(j)

                    # record indirect match
                    self.__record_letter_match(self.indirect_matches, guess[i], i)

                    # add to coloured letters
                    coloured_letters.append(guess[i])
                    
                    # add to yellow letters
                    yellow.append(guess[i])

                    break

                j = j + 1

            # record black 'yellow' indirect letter guesses
            if colour_sequence[i] == 0 and guess[i] in yellow:
                self.__record_letter_match(self.indirect_matches, guess[i], i)

            i = i + 1


        # blacklist
        self.__record_blacklist(guess, coloured_letters)


        # letter frequencies
        current_letter_frequency = dict(Counter(coloured_letters))

        # definitive letter frequency
        for letter in current_letter_frequency:
            if current_letter_frequency[letter] < guess.count(letter):
                self.definitive_frequency[letter] = current_letter_frequency[letter]
                self.potential_frequency.pop(letter, None)
                break
            else: 
                self.__record_potential_frequency(self.potential_frequency, current_letter_frequency)
        
        
        return colour_sequence



    def __validate_guess(self, guess):
        if len(guess) != 5:
            return False
        if guess in self.valid_guess_list or guess in self.valid_answer_list:
            return True
        
        return False




    # public functions

    def turn(self, guess, colour_sequence=None):

        guess = guess.casefold().strip()

        if self.__validate_guess(guess) == False:
            return False

        if self.gametype == 'unknown':
            result = self.__process_guess(guess, colour_sequence)
        else:
            result = self.__process_guess(guess)
    
        self.turn_history[self.turn_no] = {"guess": guess, "result": result}
        self.turn_no += 1

        if self.state == "win":
            return {"guess": guess, "result": result}

        if self.turn_no > self.turn_limit:
            self.state = "loss"

        return {"guess": guess, "result": result}