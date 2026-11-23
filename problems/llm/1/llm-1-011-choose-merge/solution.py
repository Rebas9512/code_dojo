def winner(ids):
    counts = {}
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    if not counts:
        return []
    return list(min(counts, key=lambda p: (-counts[p], p)))
