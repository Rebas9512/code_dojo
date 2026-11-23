import numpy as np


def validate_neighbors(X, y, k):
    X, y = np.asarray(X, dtype=float), np.asarray(y)
    scores = []
    for ids in np.array_split(np.arange(len(y)), k):
        train = np.ones(len(y), dtype=bool)
        train[ids] = False
        center = np.mean(X[train], axis=0)
        scale = np.std(X[train], axis=0)
        Z = (X - center) / np.where(scale == 0, 1, scale)
        distances = np.sum((Z[ids, None, :] - Z[train]) ** 2, axis=2)
        predictions = y[train][np.argmin(distances, axis=1)]
        scores.append(np.mean(predictions == y[ids]))
    return scores
