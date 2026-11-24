import numpy as np


def means(values, width):
    shifts = np.array(values).reshape(-1, width)
    return np.mean(shifts, axis=1)
