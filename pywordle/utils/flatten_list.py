def flatten_list(l):
    flatlist = []
    for sublist in l:
        for item in sublist:
            flatlist.append(item)
    return flatlist