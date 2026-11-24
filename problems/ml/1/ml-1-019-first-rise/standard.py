import numpy as np


def first_rise(losses):
    changes = np.diff(losses)
    increases = np.flatnonzero(changes > 0)
    return int(increases[0] + 1) if len(increases) else -1
