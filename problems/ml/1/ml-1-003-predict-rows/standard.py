import numpy as np


def predict(X, w, b):
    return np.asarray(X, dtype=float) @ w + b
