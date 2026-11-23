import numpy as np


def nonnegative(values):
    a = np.array(values)
    return np.where(a < 0, 0, a)
