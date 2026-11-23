def check(args, expected, actual):
    if not isinstance(actual, list):
        return False
    for group in actual:
        if not isinstance(group, list) or len(group) != 4 or any(type(v) is not int for v in group):
            return False
    return sorted(sorted(group) for group in actual) == sorted(sorted(group) for group in expected)
