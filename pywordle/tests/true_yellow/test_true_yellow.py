

def test_yellow_eliminate():
    true_yellow = {'a': [2,0], 'o': [1], 'n': [3]}
    wordlist = ['holds', 'swing', 'pipes', 'antsy', 'tanks', 'choke']
    bad = []
    #wordlist = ['swing']
    # should only eliminate:  holds, swing, antsy - leaving: pipes, choke, tanks
    for w in wordlist:
        #print(w)
        for i in range(0, 5):
            for ty in true_yellow:
                for index in true_yellow[ty]:
                    #print(f'{w[i]} == {ty} and {i} == {index}')
                    if w[i] == ty and i == index:
                        bad.append(w)
                        
    assert bad == ['holds', 'swing', 'antsy']

def access_index():
    true_yellow = {'a': [2,0], 'o': [1], 'n': [3]}
    for ty in true_yellow:
        for index in true_yellow[ty]:
            print(index)

# good candidate is:  true yellow, not in taken position
def test_good_candidates():
    true_yellow = {'a': [2,0], 'o': [1], 'n': [3]}
    wordlist = ['holds', 'swing', 'pipes', 'antsy', 'tanks', 'choke', 'okres', 'nancy']
    good = []
    for w in wordlist:
        for i in range(0, 5):
            for ty in true_yellow:
                if ty not in w:
                    print(ty)
                    continue
                for index in true_yellow[ty]:
                    pass
        

