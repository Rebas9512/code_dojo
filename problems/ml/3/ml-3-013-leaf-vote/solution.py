import numpy as np


def leaf(y):
    positive = np.sum(y)
    return int(positive * 2 > len(y))
