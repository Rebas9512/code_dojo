import numpy as np


def gini(labels):
    counts = np.bincount(labels)
    p = counts / len(labels)
    return ...  # 补全这里
