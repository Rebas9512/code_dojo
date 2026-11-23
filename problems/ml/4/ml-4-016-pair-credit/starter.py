import numpy as np


def pair_auc(pos, neg):
    diff = np.asarray(pos)[:, None] - np.asarray(neg)
    return np.mean(...)  # 补全这里
