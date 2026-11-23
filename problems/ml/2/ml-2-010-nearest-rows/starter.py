import numpy as np


def nearest(X, q, k):
    dist = ...  # 补全这里
    return np.argsort(dist, kind="stable")[:k]
