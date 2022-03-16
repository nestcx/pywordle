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


    assert sorted(d[2]) == sorted(['spade', 'tempo', 'mumps'])
    assert sorted(d[3]) == sorted(['moped'])

def test_length_sort():
    letters = set(['e','r', 'q', 'u', 'd', 'l'])
    d = find_intersections(wordlist, letters)
    print(d)