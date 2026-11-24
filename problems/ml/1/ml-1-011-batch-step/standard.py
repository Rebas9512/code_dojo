import numpy as np


def step(X, y, w, rate):
    X = np.asarray(X, dtype=float)
    residual = X @ w - y
    gradient = (2 / len(X)) * (X.T @ residual)
    return w - rate * gradient
