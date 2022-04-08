from collections import Counter
from pywordle.examples.maximise_similarity.word_frequency import get_highest_frequency

"""

A 'cleanup' word refers to a word that eliminates as many letters as possible that
are in the final word, when presented with a situation where there are multiple
similar answers with only a few letters difference between them. In such a situation
it is most efficient to eliminate those few letters of difference between the
remaining words by playing a word that contains as many of those letters as possible.

Example:  
- Word: 'ratty'
- Direct Matches: {'a': [1], 't': [2, 3], 'y': [4]} 
- Indirect Matches: {}
- Remaining Words:  ['catty', 'patty', 'ratty', 'tatty']
- Definitive Frequency: {} 


We should play a word that contains as many letters from the set:
[c, p, r, t]

How do we calculate this set?

1.  get the letter frequency in the remaining words (rwlf):

c: 1
p: 1
r: 1
a: 4
y: 4
t: 9


2.  get the letter frequency in the direct matches (dmlf):

a: 1
y: 1
t: 2


3.  (_get_cleanup_letter_set)

if there is a remaining word with a letter that isn't in direct matches,
or if a remaining word has more than 2 t's, 1 y, or 1 a, then that letter 
could appear in the final word.

compare rwlf to dmlf and if the frequencies don't match that means that letter could 
exist in the answer.

eg:  

rwlf[t] == dmlf[t] * len(remaining_words)
   9    ==    8
't' is valid.

rwlf[y] == dmlf[y] * len(remaining_words)
   4    ==    4
'y' is not valid. There are no more y's to match.


do this for each letter in rwlf.
now we have the set:  [c, p, r, t]

the answer will have at least one of those letters that is higher than the frequency
currently matched. i.e., the answer might have three t's, but not 2.


4. Find words that have the letters in them.

For each word in the wordlist, see how many letters are from the letter set are
present in it.

The intersection() method returns a set that contains the similarity between 
two sets, i.e. letter_set.intersection(word)


5. Meet certain conditions to play certain cleanup word.

"""


def _get_remaining_answers_letter_frequency(remaining_words):
    return Counter(''.join(remaining_words))


def _get_direct_matches_letter_frequency(direct_matches):
    dm_freq = {}
    for m in direct_matches:
        dm_freq[m] = len(direct_matches[m])
    return dm_freq


def _get_cleanup_letter_set(remaining_answers, dm_freq, rm_freq):

    # start with a set of all letters from remaining words
    # add letters to list 'x' that could be in the word.
    letters = set(''.join(remaining_answers))
    x = []

    for l in letters:
        if l not in dm_freq:
            x.append(l)
        else:
            if rm_freq[l] != dm_freq[l] * len(remaining_answers):
                x.append(l)
    
    return x

def _get_cleanup_words(wordlist, letters):

    d = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

    for w in wordlist:
        x = len(set(''.join(letters)).intersection(w))
        d[x].append(w)

    return d


def _get_green_letters_count(direct_matches):
    count = 0
    for green_indexes in direct_matches.values():
        count += len(green_indexes)
    return count



# DEFINE CONSTS

def cleanup(game):

    # outright no cleanup if on first turn or only two answers left
    if game.turn_no < 2 or len(game.get_remaining_answers) <= 2:
        return False

    cs = game.turn_history[game.turn_no-1]["result"]
    green_count = cs.count(1)

    if not(green_count >= 2 and game.turn_no < 5):
        return False

    rwlf = _get_remaining_answers_letter_frequency(game.get_remaining_answers)
    dmlf = _get_direct_matches_letter_frequency(game.direct_matches)
    letters = _get_cleanup_letter_set(game.get_remaining_answers, dmlf, rwlf)
    cleanup_words = _get_cleanup_words(game.valid_guess_list, letters)

    word = ''
    for i in range (5, 0, -1):
        if cleanup_words[i] != []:
            word = get_highest_frequency(cleanup_words[i], cleanup_words[i], game.true_yellow, game.turn_no)
            break

    return word








