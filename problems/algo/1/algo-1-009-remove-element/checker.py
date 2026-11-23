def check(args, expected, actual):
    if not isinstance(actual, list) or len(actual) != 2:
        return False
    size, kept = actual
    if type(size) is not int or size != expected[0] or not isinstance(kept, list):
        return False
    return all(type(x) is int for x in kept) and sorted(kept) == sorted(expected[1])
