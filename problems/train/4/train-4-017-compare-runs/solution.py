def first_drift(reference, observed, tol):
    for i, (wanted, actual) in enumerate(zip(reference, observed), 1):
        if abs(wanted - actual) > tol:
            return i
    if len(reference) != len(observed):
        return min(len(reference), len(observed)) + 1
    return 0
