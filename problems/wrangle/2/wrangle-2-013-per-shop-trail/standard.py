import numpy as np


def running_sales(rows):
    return np.cumsum(rows, axis=1)
