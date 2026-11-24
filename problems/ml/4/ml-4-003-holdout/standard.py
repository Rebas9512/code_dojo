import numpy as np


def holdout(X, y, count, seed):
    X, y = np.asarray(X), np.asarray(y)
    order = np.random.default_rng(seed).permutation(len(y))
    test, train = order[:count], order[count:]
    return X[train], y[train], X[test], y[test]
