import numpy as np


def binary_loss(z, y):
    z = np.asarray(z, dtype=float)
    y = np.asarray(y)
    p = 1 / (1 + np.exp(-z))
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
