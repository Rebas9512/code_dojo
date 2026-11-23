import numpy as np


def adjust(rows, offsets):
    return np.array(rows) + np.array(offsets).reshape(-1, 1)
