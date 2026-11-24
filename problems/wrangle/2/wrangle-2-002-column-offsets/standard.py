import numpy as np


def calibrate(rows, offsets):
    a = np.array(rows)
    return a + np.array(offsets)
