import numpy as np


def binary_loss(z, y):
    z = np.asarray(z, dtype=float)
    y = np.asarray(y)
    return np.mean(np.logaddexp(0, z) - y * z)
