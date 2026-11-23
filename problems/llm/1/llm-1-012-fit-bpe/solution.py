def merge_once(ids, pair, fresh):
    result = []
    i = 0
    while i < len(ids):
        if ids[i:i + 2] == pair:
            result.append(fresh)
            i += 2
        else:
            result.append(ids[i])
            i += 1
    return result


def winner(ids):
    counts = {}
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    if not counts:
        return []
    return list(min(counts, key=lambda p: (-counts[p], p)))


def fit_bpe(ids, k):
    rules = []
    for step in range(k):
        pair = winner(ids)
        if not pair:
            break
        rules.append(pair)
        ids = merge_once(ids, pair, 256 + step)
    return rules
