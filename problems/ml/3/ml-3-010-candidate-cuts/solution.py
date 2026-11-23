import numpy as np


def candidates(x):
    values = np.unique(x)
    return (values[1:] + values[:-1]) / 2
