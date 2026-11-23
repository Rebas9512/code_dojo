import numpy as np


def prepare(X, train_ids, test_ids):
    X = np.asarray(X, dtype=float)
    train = X[train_ids]
    scale = np.std(train, axis=0)
    return (X[test_ids] - np.mean(train, axis=0)) / np.where(scale == 0, 1, scale)
