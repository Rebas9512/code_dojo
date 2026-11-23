import numpy as np


def mse(pred, y):
    diff = np.asarray(pred, dtype=float) - y
    return np.mean(diff ** 2)
