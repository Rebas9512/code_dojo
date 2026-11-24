import numpy as np


def errors(pred, y):
    residual = np.asarray(pred, dtype=float) - y
    return residual**2
