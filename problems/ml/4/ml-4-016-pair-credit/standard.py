import numpy as np


def pair_auc(pos, neg):
    positive = np.asarray(pos)[:, None]
    negative = np.asarray(neg)
    return np.mean((positive > negative) + 0.5 * (positive == negative))
