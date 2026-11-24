import numpy as np


def binary_loss(z, y):
    z = np.asarray(z, dtype=float)
    y = np.asarray(y)
    signed_score = (1 - 2 * y) * z
    return np.mean(np.logaddexp(0, signed_score))
