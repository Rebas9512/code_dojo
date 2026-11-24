import numpy as np


def recall(cm):
    table = np.asarray(cm)
    actual_positive = np.sum(table[1])
    return float(table[1, 1] / actual_positive) if actual_positive else 0.0
