def check(args, expected, actual):
    s = args[0]
    if not isinstance(actual, str):
        return False
    if not actual:
        return 2 * max(s.count(c) for c in set(s)) > len(s) + 1
    return sorted(s) == sorted(actual) and all(a != b for a, b in zip(actual, actual[1:]))
