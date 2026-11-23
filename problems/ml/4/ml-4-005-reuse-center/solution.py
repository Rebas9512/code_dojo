import numpy as np


def apply_center(train, test):
    center = np.mean(train, axis=0)
    return np.asarray(test, dtype=float) - center
