from collections import Counter



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


def get_rm_freq(remaining_words):
    return Counter(''.join(remaining_words))


def get_dm_freq(direct_matches):
    dm_freq = {}
    for m in direct_matches:
        dm_freq[m] = len(direct_matches[m])
    return dm_freq


def find_intersections(wordlist, letters):
    d = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
    for w in wordlist:
        x = len(letters.intersection(w))
        d[x].append(w)
    return d
