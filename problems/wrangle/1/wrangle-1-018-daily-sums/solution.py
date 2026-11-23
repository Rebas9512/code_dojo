import numpy as np


def daily(rows):
    return np.sum(np.array(rows), axis=0)
