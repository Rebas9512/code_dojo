def check(args, expected, actual):
    if not isinstance(actual, str) or any(c not in 'abc' for c in actual):
        return False
    large = max(args)
    others = sum(args) - large
    length = others + min(large, 2 * (others + 1))
    return len(actual) == length and all(actual.count(c) <= n and c*3 not in actual for c, n in zip('abc', args))
