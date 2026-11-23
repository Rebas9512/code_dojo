def check(args, expected, actual):
    if not isinstance(actual, list):
        return False
    if not all(isinstance(group, list) and all(isinstance(word, str) for word in group) for group in actual):
        return False
    return sorted(sorted(group) for group in actual) == sorted(sorted(group) for group in expected)
