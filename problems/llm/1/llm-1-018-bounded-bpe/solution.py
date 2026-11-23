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


def apply_rules(ids, rules):
    for rank, pair in enumerate(rules):
        ids = merge_once(ids, pair, 256 + rank)
    return ids


def bounded_bpe(text, rules):
    result = []
    for i, part in enumerate(text.split("<end>")):
        if i:
            result.append(1000)
        result.extend(apply_rules(list(part.encode("utf-8")), rules))
    return result
