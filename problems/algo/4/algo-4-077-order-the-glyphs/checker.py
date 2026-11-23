def check(args, expected, actual):
    if not isinstance(actual, str):
        return False
    if not expected:
        return actual == ""
    words = args[0]
    letters = set("".join(words))
    if len(actual) != len(letters) or set(actual) != letters:
        return False
    rank = {ch: i for i, ch in enumerate(actual)}
    for first, second in zip(words, words[1:]):
        for a, b in zip(first, second):
            if a != b:
                if rank[a] >= rank[b]:
                    return False
                break
        else:
            if len(first) > len(second):
                return False
    return True
