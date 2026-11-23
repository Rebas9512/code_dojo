def check(args, expected, actual):
    k, above, left = args
    if not expected:
        return actual == []
    if not isinstance(actual, list) or len(actual) != k:
        return False
    positions = {}
    for r, row in enumerate(actual):
        if not isinstance(row, list) or len(row) != k:
            return False
        for c, value in enumerate(row):
            if type(value) is not int or not 0 <= value <= k:
                return False
            if value:
                if value in positions:
                    return False
                positions[value] = (r, c)
    return (len(positions) == k
            and all(positions[a][0] < positions[b][0] for a, b in above)
            and all(positions[a][1] < positions[b][1] for a, b in left))
