def check(args, expected, actual):
    if not isinstance(actual, list) or len(actual) != len(expected):
        return False
    for wanted, got in zip(expected, actual):
        if wanted is None:
            if got is not None:
                return False
        elif not isinstance(got, list) or len(got) != 2 or got[0] != wanted[0] or got[1] not in (0, 1):
            return False
        elif wanted[0] and wanted[1] != got[1]:
            return False
    return True
