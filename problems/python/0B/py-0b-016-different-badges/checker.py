def check(args, expected, actual) -> bool:
    if not isinstance(actual, list) or len(actual) != 2:
        return False
    for wanted, given in zip(expected, actual):
        if not isinstance(given, list) or not all(type(x) is int for x in given):
            return False
        if sorted(given) != sorted(wanted):
            return False
    return True
