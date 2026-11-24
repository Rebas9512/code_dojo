import numpy as np


def fold_ids(n, k):
    result = np.empty(n, dtype=int)
    for i, rows in enumerate(np.array_split(np.arange(n), k)):
        result[rows] = i
    return result
