from new_ms_functions import elim_m, get_rm_freq, get_dm_freq

def test_rmf():
    remaining_answers = ['catch', 'hatch', 'match', 'patch', 'watch']
    assert get_rm_freq(remaining_answers) == {"c": 6, "h": 6, "a": 5, "t": 5, "m": 1, "w": 1, "p": 1}

def test_dmf():
    direct_matches = {'a': [1, 2], 't': [2], 'c': [3], 'h': [4]}
    assert len(direct_matches['a']) == 2
    assert len(direct_matches['t']) == 1
    assert len(direct_matches) == 4

    assert get_dm_freq(direct_matches) == {'a': 2, 't': 1, 'c': 1, 'h': 1}


def test_patch():
    remaining_answers = ['catch', 'hatch', 'match', 'patch', 'watch']
    rm_freq = {"c": 6, "h": 6, "a": 5, "t": 5, "m": 1, "w": 1, "p": 1}
    dm_freq = {'a': 1, 't': 1, 'c': 1, 'h': 1}

    rem = elim_m(remaining_answers, dm_freq, rm_freq)

    assert sorted(rem) == sorted(['c', 'h', 'm', 'p', 'w'])


def test_ratty():
    remaining_answers = ['catty', 'patty', 'ratty', 'tatty']
    direct_matches = {'a': [1], 't': [2, 3], 'y': [4]}

    rm_freq = get_rm_freq(remaining_answers)
    dm_freq = get_dm_freq(direct_matches)

    assert sorted(elim_m(remaining_answers, dm_freq, rm_freq)) == sorted(['c', 'p', 'r', 't'])

def test_shave():
    remaining_answers = ['shade', 'shake', 'shame', 'shape', 'shave']
    direct_matches = {'s': [0], 'h': [1], 'a': [2], 'e': [4]}

    rm_freq = get_rm_freq(remaining_answers)
    dm_freq = get_dm_freq(direct_matches)

    assert sorted(elim_m(remaining_answers, dm_freq, rm_freq)) == sorted(['d', 'k', 'm', 'p', 'v'])
