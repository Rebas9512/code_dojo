import numpy as np


def update(X, y, w, b, rate):
    X = np.asarray(X, dtype=float)
    z = X @ w + b
    error = np.exp(-np.logaddexp(0, -z)) - y
    weights = w - rate * (X.T @ error) / len(X)
    return np.append(weights, b - rate * np.mean(error))
