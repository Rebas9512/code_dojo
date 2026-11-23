import numpy as np


def design(X):
    rows = np.asarray(X, dtype=float)
    return np.column_stack((rows, ...))  # 补全这里
