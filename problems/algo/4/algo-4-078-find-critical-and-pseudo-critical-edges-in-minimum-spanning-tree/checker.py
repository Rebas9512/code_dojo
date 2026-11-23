def check(args, expected, actual):
    if not isinstance(actual, list) or len(actual) != 2:
        return False
    for group, wanted in zip(actual, expected):
        if not isinstance(group, list) or any(type(i) is not int for i in group):
            return False
        if sorted(group) != sorted(wanted):
            return False
    return True
