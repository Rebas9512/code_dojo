import numpy as np


def confusion(truth, pred, K):
    table = np.zeros((K, K), dtype=int)
    for actual, guess in zip(truth, pred):
        table[actual, guess] += 1
    return table
