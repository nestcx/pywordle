import random
from collections import Counter
from pywordle.helpers.elimination import eliminate_words
from pywordle.pywordle import DEFAULT_ANSWER_LIST, DEFAULT_GUESS_LIST

class Wordle():

    valid_guess_list = ()
    valid_answer_list = ()

    def __init__(self, gametype = 'random', word = None, word_index = None, turn_limit = 6, valid_guess_list=DEFAULT_GUESS_LIST, valid_answer_list=DEFAULT_ANSWER_LIST):

        Wordle.valid_guess_list = self.__read_wordlist(valid_guess_list)
        Wordle.valid_answer_list = self.__read_wordlist(valid_answer_list)

        if gametype == 'random':
            self.word = self.__get_random_word()
        elif gametype == 'unknown':
            self.word = None
        elif gametype == 'select':
            self.word = word
        elif gametype == 'index':
            self.word = Wordle.valid_answer_list[word_index]

        self.state = "active"
        self.turn_no = 1
        self.turn_limit = turn_limit

        self.direct_matches = {}
        self.indirect_matches = {}
        self.potential_frequency = {}
        self.definitive_frequency = {}
        self.blacklist = []


    # getters

    @property
    def get_remaining_answers(self):
        data = {}
        data["direct_matches"] = self.direct_matches
        data["indirect_matches"] = self.indirect_matches
        data["potential_frequency"] = self.potential_frequency
        data["definitive_frequency"] = self.definitive_frequency
        data["blacklist"] = self.blacklist

        return eliminate_words(data, Wordle.valid_answer_list)

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
    def debug_info(self):
        out = ""
        out += f'Word: {self.word} \n'
        out += f'Gamestate: {self.state} - {self.turn_no}/{self.turn_limit} \n'
        out += f'Direct Matches: {self.direct_matches} \n'
        out += f'Indirect Matches: {self.indirect_matches} \n'
        out += f'Blacklist: {self.blacklist} \n'
        out += f'Potential Frequency: {self.potential_frequency} \n'
        out += f'Definitive Frequency: {self.definitive_frequency} \n'
        out += f'Remaining Answers: {len(self.get_remaining_answers)}/{len(Wordle.valid_answer_list)} \n'
        return out


    # private functions

    def __read_wordlist(self, wordlist):
        f = open(wordlist, 'r')
        wordlist = f.read().splitlines()
        f.close()
        return wordlist
        

    def __get_random_word(self):
        return(random.choice(Wordle.valid_answer_list))

    
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

    def __process_guess(self, guess):

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
            if guess[i] == self.word[i]:
                position_skip.append(i)
                colour_sequence[i] = 1

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

                if guess[i] == self.word[j]:
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
        if guess in Wordle.valid_guess_list or guess in Wordle.valid_answer_list:
            return True
        
        return False

    def __validate_colour_sequence(self, colour_sequence):
        return True





    # public functions

    def turn(self, guess, colour_sequence=None):

        guess = guess.casefold().strip()

        if self.__validate_guess(guess) == False:
            return False

        if colour_sequence != None:
            if self.__validate_colour_sequence(colour_sequence) == False:
                return False

            self.__process_guess(guess, colour_sequence)
        else:
            result = self.__process_guess(guess)

        self.turn_no += 1

        if self.state == "win":
            return {"guess": guess, "result": result}

        if self.turn_no > self.turn_limit:
            self.state = "loss"

        return {"guess": guess, "result": result}