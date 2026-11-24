import numpy as np


def nearest(X, q, k):
    dist = np.sum((np.asarray(X, dtype=float) - q) ** 2, axis=1)
    return np.argsort(dist, kind="stable")[:k]
