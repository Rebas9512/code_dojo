import numpy as np


def misses(truth, pred):
    y, p = np.asarray(truth), np.asarray(pred)
    return int(np.sum(np.logical_and(y == 1, p == 0)))
