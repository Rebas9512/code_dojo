def count_pair(ids, pair):
    total = 0
    for i in range(len(ids) - 1):
        if ids[i:i + 2] == pair:
            total += 1
    return total
