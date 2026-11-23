import numpy as np


def validate(y, k):
    y = np.asarray(y, dtype=float)
    scores = []
    for rows in np.array_split(np.arange(len(y)), k):
        train = np.ones(len(y), dtype=bool)
        train[rows] = False
        prediction = np.mean(y[train])
        scores.append(np.mean((y[rows] - prediction) ** 2))
    return scores
