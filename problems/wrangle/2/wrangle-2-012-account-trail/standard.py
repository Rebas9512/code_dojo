import numpy as np


def balances(changes):
    return np.cumsum(changes)
