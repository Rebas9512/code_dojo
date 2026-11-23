import numpy as np


def epoch(X, y, w, rate, size):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.asarray(w, dtype=float)
    for start in range(0, len(X), size):
        block = X[start:start + size]
        target = y[start:start + size]
        grad = 2 * block.T @ (block @ w - target) / len(block)
        w = w - rate * grad
    return w
