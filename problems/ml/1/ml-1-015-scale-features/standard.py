import numpy as np


def standardize(X):
    X = np.asarray(X, dtype=float)
    scale = np.std(X, axis=0)
    return (X - np.mean(X, axis=0)) / np.where(scale == 0, 1, scale)
