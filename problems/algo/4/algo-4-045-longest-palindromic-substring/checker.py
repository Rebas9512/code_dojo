def check(args, expected, actual):
    return (isinstance(actual, str) and len(actual) == len(expected)
            and actual in args[0] and actual == actual[::-1])
