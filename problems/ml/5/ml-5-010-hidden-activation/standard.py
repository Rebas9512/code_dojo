import numpy as np


def hidden(X, W1, b1):
    z = np.asarray(X, dtype=float) @ W1 + b1
    return np.tanh(z)
