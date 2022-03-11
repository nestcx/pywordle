from collections import Counter


def __test_indirect_matches(indirect_matches, word):
    for x in indirect_matches:

        if x not in word:
            return False

        for index in indirect_matches[x]:
            if word[index] == x:
                return False

    return True


def __test_direct_matches(direct_matches, word):
    for x in direct_matches:

        if x not in word:
            return False

        for index in direct_matches[x]:
            if word[index] != x:
                return False

    return True
        

# return true if word has no blacklisted letters.
def __test_blacklist(blacklist, word):
    for b in blacklist:
        if b in word:
            return False
    return True


def __test_letter_frequency(plf, dlf, word):

    word_dict =  dict(Counter(word))

    for letter in dlf:
        if word_dict[letter] != dlf[letter]:
            return False
    for letter in plf:
        if word_dict[letter] < plf[letter]:
                return False

    return True

# returns an answers list after putting data through tests, eliminating words
# from complete words list
def eliminate_words(data, lines):

    remaining_answers = []

    for word in lines:
        if __test_blacklist(data["blacklist"], word) == False:
            continue

        if __test_direct_matches(data["direct_matches"], word) == False:
            continue

        if __test_indirect_matches(data["indirect_matches"], word) == False:
            continue

        if __test_letter_frequency(data["potential_frequency"], data["definitive_frequency"], word) == False:
            continue

        
        remaining_answers.append(word)
    
    return remaining_answers