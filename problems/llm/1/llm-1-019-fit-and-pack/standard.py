def merge_once(ids, pair, fresh):
    result = []
    i = 0
    while i < len(ids):
        if ids[i : i + 2] == pair:
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


def apply_rules(ids, rules):
    for rank, pair in enumerate(rules):
        ids = merge_once(ids, pair, 256 + rank)
    return ids


def fit_and_pack(corpus, text, k):
    rules = fit_bpe(list(corpus.encode("utf-8")), k)
    tokens = []
    for i, part in enumerate(text.split("<end>")):
        if i:
            tokens.append(1000)
        tokens.extend(apply_rules(list(part.encode("utf-8")), rules))
    return tokens
