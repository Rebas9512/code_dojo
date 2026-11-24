import numpy as np


def vote(X, labels, q, k):
    dist = np.sum((np.asarray(X, dtype=float) - q) ** 2, axis=1)
    rows = np.argsort(dist, kind="stable")[:k]
    votes = np.bincount(np.asarray(labels)[rows])
    return int(np.argmax(votes))
