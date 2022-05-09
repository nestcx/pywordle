from collections import Counter


def __test_indirect_matches(indirect_matches, answer):
    for x in indirect_matches:

        if x not in answer:
            return False

        for index in indirect_matches[x]:
            if answer[index] == x:
                return False

    return True


def __test_direct_matches(direct_matches, answer):
    for x in direct_matches:

        if x not in answer:
            return False

        for index in direct_matches[x]:
            if answer[index] != x:
                return False

    return True
        

# return true if answer has no blacklisted letters.
def __test_blacklist(blacklist, answer):
    for b in blacklist:
        if b in answer:
            return False
    return True


def __test_letter_frequency(plf, dlf, answer):

    answer_dict =  dict(Counter(answer))

    for letter in dlf:
        if answer_dict[letter] != dlf[letter]:
            return False
    for letter in plf:
        if answer_dict[letter] < plf[letter]:
                return False

    return True

# returns an answers list after putting data through tests, eliminating words
# from complete words list
def eliminate_answers(data, answers):

    remaining_answers = []

    for answer in answers:
        if __test_blacklist(data["blacklist"], answer) == False:
            continue

        if __test_direct_matches(data["direct_matches"], answer) == False:
            continue

        if __test_indirect_matches(data["indirect_matches"], answer) == False:
            continue

        if __test_letter_frequency(data["potential_frequency"], data["definitive_frequency"], answer) == False:
            continue
        
        remaining_answers.append(answer)
    
    return remaining_answers