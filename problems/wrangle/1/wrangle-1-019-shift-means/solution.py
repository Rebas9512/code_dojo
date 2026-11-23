import numpy as np


def means(values, width):
    return np.mean(np.array(values).reshape(-1, width), axis=1)
