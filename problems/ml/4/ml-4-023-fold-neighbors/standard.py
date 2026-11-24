import numpy as np


def validate_neighbors(X, y, k):
    X, y = np.asarray(X, dtype=float), np.asarray(y)
    scores = []
    for ids in np.array_split(np.arange(len(y)), k):
        train = np.ones(len(y), dtype=bool)
        train[ids] = False
        train_X = X[train]
        center = np.mean(train_X, axis=0)
        scale = np.std(train_X, axis=0)
        scale = np.where(scale == 0, 1, scale)
        train_scaled = (train_X - center) / scale
        test_scaled = (X[ids] - center) / scale
        distances = np.sum((test_scaled[:, None, :] - train_scaled) ** 2, axis=2)
        predictions = y[train][np.argmin(distances, axis=1)]
        scores.append(np.mean(predictions == y[ids]))
    return scores
