import numpy as np


def step(X, y, w, rate):
    X = np.asarray(X, dtype=float)
    gradient = 2 * X.T @ (X @ w - y) / len(X)
    return ...  # 补全这里
