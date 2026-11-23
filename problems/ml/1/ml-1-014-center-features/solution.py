import numpy as np


def center(X):
    X = np.asarray(X, dtype=float)
    return X - np.mean(X, axis=0)
