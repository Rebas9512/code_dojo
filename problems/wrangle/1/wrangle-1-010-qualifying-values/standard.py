import numpy as np


def qualified(values, limit):
    a = np.array(values)
    return a[a >= limit].tolist()
