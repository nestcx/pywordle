import random
from collections import Counter
from pywordle.helpers.elimination import eliminate_answers
from pywordle import DEFAULT_ANSWER_LIST, DEFAULT_GUESS_LIST
from pywordle.utils.flatten_list import flatten_list
import copy



class Wordle():

    '''
    A class used to represent a Wordle game instance.


    Attributes
    ----------

    ** word lists **
    - files imported in __init__.py, set to a constant, and imported.

    valid_guess_list : list (default DEFAULT_GUESS_LIST)
        a list of allowable guesses.

    valid_answer_list : list (default DEFAULT_ANSWER_LIST)
        a list of allowable answers.

    gametype : str (default 'random')

        valid types:
        - 'random': game selects a random answer from the answers list.

        - 'unknown': the answer attribute is not set. process_guess does not 
           return a colour sequence - it must be passed in as an argument.

        - 'select': 
            - additional required argument: answer.
            - sets the answer attribute to the constructor argument answer.

        - 'index': 
            - additional required argument: answer_index.
            - sets the answer attribute to the answer from the answerslist at 
              index defined by the constructor argument answer_index.

    answer : str (default None)
        answer the player must guess in order to win.
    
    turn_no : int (default 1)
        turn number the game is currently on.

    turn_limit : int (default 6)
        number of turns allowed before the game ends (state = 'loss' or 'win')

    turn_history : dict
        data record from each turn including turn number, guess, and resulting
        colour sequence.
        example:
            { 1: {"guess": "tried", "result": [0, 0, 0, 2, 0]},
              2: {"guess": "hello", "result": [0, 1, 1, 1, 1]} }

    state : str (default 'active')
        valid types: ['active', 'win', 'loss']


   ** the following data structures are used in order to calculate the list of
    remaining potential answers from the answers list. **

    direct_matches : dict
        data record of every direct (green) match that has been guessed.
        populated in process_guess().
        example:
            {'e': [1], 'l': [2, 3], 'o': [4]}
            interpreted as, the letter 'e' is at index 1 in the answer.

        this record is ONLY populated from the result of a guess. it is not
        populated based on the letters of what answers remain.
        i.e., if the remaining answers are: ['chase', 'plate'], even though
        'a' and 'e' must be at indexes 2 and 4 respectively, that information
        is not added to direct_matches, as this would be redundant, since
        direct_matches, and the following data structures, create the
        remaining answers list. This applies for the indirect_matches,
        potential_frequency, and definitive_frequency data records.

    indirect_matches : dict
        data record of every indirect (yellow) match that has been guessed.
        populated in process_guess().
        example:
            {'s': [4, 1]}
            interpreted as, the letter 's' has turned yellow at indexes 4, 1.

        when a letter turns green at one of those indexes, i.e. at index 1
        there is a direct match for the letter 'p', the indirect_matches
        list is NOT updated to reflect this. it is a historical record.

    ** letter frequencies **
        - definitive frequency:  the word must have *exactly* n of the letter.
            - ascertained from a single guess in process_guess.
            - in a guess, if a letter appears at least twice, and n are
              coloured (yellow or green) AND at least another is black, then
              there must be exactly n of that letter in the answer.
        - potential frequency:  the word must have at *least* n of the letter.
            - ascertained from a single guess in process_guess.
            - in a guess, if n of a letter is coloured (yellow or green) and 
              that also does not appear black in the same guess, then there 
              could potentially be n or more of that letter in the answer.
              
    potential_frequency : dict
        populated in process_guess().
        example:
            {'s': 1}
            intepreted as, there is at least 1 's' in the answer.

    definitive_frequency : dict
        populated in process_guess().
        example:
            {'e': 2}
            interpreted as, there are exactly 2 of letter 'e' in the answer.

    note: when a definitive_frequency is recorded, that letter/key is removed
          from potential_frequency

    blacklist : list
        when a letter returns black (not present in answer), it is added 
        to this list.


    Properties
    ----------
    get_remaining_answers : list
        returns a list of possible remaining answers.
        example: ['apple', 'ample', 'achey']

    get_keyboard_data : dict
        returns state of letter colours, used to create coloured keyboards
        for visual feedback.
        example: {'green': {'a', 'l'}, 'yellow': {'k'}, 'black': ['h', 'e']}
        
    get_keystrokes : list
        returns a list of every letter that has guessed.
        example: ['a', 'e', 'w']

    gamestate : dict
        the 'gamestate' is defined by the state of the instance attributes.
        these attributes are copied and returned in a dictionary.

    true_yellow : dict
        returns a dict of letters that are considered 'true yellow'.
        a 'true yellow' letter is a letter that has been 'yellowed' and has
        not been found (turned green) yet.
        example: {'e': [1], 'i': [1]}


    Methods
    ------
    __load_gamestate (dict gamestate)
        takes a dictionary of instance attributes (provided by gamestate 
        property)
        and copies data to existing attributes.

    __read_wordlist : list
        opens a wordlist file and return the data as a list.

    __get_random_word : str
        returns a random answer from the answers list.

    __record_letter_match (dict dict, str letter, int index)
        records direct and indirect matches in self.direct_matches and
        self.indirect_matches respectively.
        called from process_guess.

    __record_potential_frequency (dict letters)
        records potential frequencies in self.potential_frequency.
        called from process_guess.

    __record_blacklist (str guess, dict coloured_letters)
        records blacklisted letters in self.blacklist. 
        called from process_guess.

    __process_guess (str guess, list colour_sequence=None) : list
       processes a single guess and updates the data for the following 
       attributes through the following methods:
       - self.direct_matches (__record_letter_match)
       - self.indirect_matches (__record_letter_match)
       - self.definitive_frequency (occurs in function body)
       - self.potential_frequency (__record_potential_frequency)
       returns a colour sequence (list) if not already provided as an argument

    __validate_guess (str guess)
        check the guess is in the guesses list.

    turn
        processes a single turn (only public function in Wordle class)



    '''

    def __init__(self, gamestate = None, gametype = 'random', answer = None, answer_index = None, turn_limit = 6, valid_guess_list = DEFAULT_GUESS_LIST, valid_answer_list = DEFAULT_ANSWER_LIST):

        self.valid_guess_list = self.__read_wordlist(valid_guess_list)
        self.valid_answer_list = self.__read_wordlist(valid_answer_list)
        
        self.gametype = None
        self.answer = None
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
                self.answer = self.__get_random_word()
            elif self.gametype == 'unknown':
                self.answer = None
            elif self.gametype == 'select':
                self.answer = answer
            elif self.gametype == 'index':
                self.answer = self.valid_answer_list[answer_index]

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

        return eliminate_answers(data, self.valid_answer_list)


    @property
    def get_keyboard_data(self):
        '''
        built from direct_matches, indirect_matches, blacklist attributes, 
        therefore if a letter is recorded yellow and later found green, it will
        no longer show in yellow.
        used for creating coloured feedback keyboards.
        '''
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
        gamestate["answer"] = self.answer
        gamestate["turn_no"] = self.turn_no
        gamestate["turn_limit"] = self.turn_limit
        gamestate["state"] = self.state
        gamestate["direct_matches"] = self.direct_matches
        gamestate["indirect_matches"] = self.indirect_matches
        gamestate["potential_frequency"] = self.potential_frequency
        gamestate["definitive_frequency"] = self.definitive_frequency
        gamestate["blacklist"] = self.blacklist

        return gamestate


    @property
    def true_yellow(self):

        yellow_letters = copy.deepcopy(self.indirect_matches)
        dm_indexes = flatten_list(self.direct_matches.values())
        rem = self.get_remaining_answers
        jrem = ''.join(rem)

        yk = list(yellow_letters.keys())

        for letter in yk:

            if letter in self.direct_matches:
                if len(self.direct_matches[letter]) * len(rem) == jrem.count(letter):
                    yellow_letters.pop(letter)
                    continue

            for index in yellow_letters[letter]:
                if index in dm_indexes:
                    yellow_letters[letter].remove(index)

        return yellow_letters


    # private functions

    def __load_gamestate(self, gamestate):
        self.gametype = gamestate["gametype"]
        self.answer = gamestate["answer"]
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

    
    # record direct and indirect matches
    def __record_letter_match(self, dict, letter, index):
        if letter not in dict:
            dict[letter] = []
    
        if index not in dict[letter]:
            dict[letter].append(index)


    def __record_potential_frequency(self, letters):
        for x, i in letters.items():
            if (self.potential_frequency.get(x) == None or self.potential_frequency[x] < i):
                self.potential_frequency[x] = i
            

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
        if guess == self.answer:
            self.state = "win"

        # direct matches
        i = 0
        while i < 5:
            if (self.gametype != 'unknown' and guess[i] == self.answer[i]) or colour_sequence[i] == 1:
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

                if (self.gametype != 'unknown' and guess[i] == self.answer[j]) or colour_sequence[i] == 2:
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


        # letter frequencies for current turn
        current_letter_frequency = dict(Counter(coloured_letters))

        # rercod letter frequencies
        for letter in current_letter_frequency:
            # definitive letter frequency
            if current_letter_frequency[letter] < guess.count(letter):
                self.definitive_frequency[letter] = current_letter_frequency[letter]
                self.potential_frequency.pop(letter, None)
                break
            else: 
                # potential letter frequency
                self.__record_potential_frequency(current_letter_frequency)
        
        
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