from collections import Counter


def check(args, expected, actual):
    a, b, k = args
    if not isinstance(actual, list) or len(actual) != k:
        return False
    left, right = Counter(a), Counter(b)
    seen = Counter()
    for pair in actual:
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or any(type(x) is not int for x in pair)
        ):
            return False
        x, y = pair
        seen[x, y] += 1
        if seen[x, y] > left[x] * right[y]:
            return False
    return sorted(map(sum, actual)) == sorted(map(sum, expected))
