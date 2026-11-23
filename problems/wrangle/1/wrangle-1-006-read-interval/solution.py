import numpy as np


def interval(values, start, stop):
    a = np.array(values)
    return a[start:stop].tolist()
