from new_ms_functions import find_intersections
import random

wordlist = [
'shawl', 'fluff', 'drill', 'clean', 'awful', 
'dowry', 'hatch', 'endow', 'stock', 'spelt', 
'prize', 'spade', 'ulcer', 'brown', 'tasty', 
'tempo', 'smith', 'tapir', 'moped', 'mumps'
]

def test_intersection():
    letters = set(['d', 'k', 'm', 'p', 'v'])

    z = letters.intersection('moved')
    assert sorted(z) == sorted(['d', 'm', 'v'])

    z = letters.intersection('piles')
    assert sorted(z) == sorted(['p'])

    z = letters.intersection('ddddk')
    assert len(z) == 2


def find_intersections(wordlist, letters):
    d = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
    for w in wordlist:
        x = len(letters.intersection(w))
        d[x].append(w)
    return d


def test_length_sort():
    letters = set(['d', 'k', 'm', 'p', 'v'])

    d = find_intersections(wordlist, letters)

    assert sorted(d[2]) == sorted(['spade', 'tempo', 'mumps'])
    assert sorted(d[3]) == sorted(['moped'])


def test_length_sort():
    letters = set(['e','r', 'q', 'u', 'd', 'l'])
    d = find_intersections(wordlist, letters)
    print(d)


def test_get_best_word():
    word = ''
    d = {0: ['hatch', 'stock', 'tasty', 'smith'], 2: ['fluff', 'clean', 'awful'], 3: ['drill'], 4: ['ulcer', 'goals'], 5: []}
    for i in range(5, 0, -1):
        if d[i] != []:
            word = d[i][0]
            break
    
    assert word == 'ulcer'


def test_get_green_count():
    c = 0
    direct_matches = {'a': [1], 't': [2, 3], 'y': [4]}
    for d in direct_matches:
        c += len(direct_matches[d])

    assert c == 4