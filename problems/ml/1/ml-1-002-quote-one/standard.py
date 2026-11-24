import numpy as np


def quote(x, w, b):
    weighted = np.asarray(x, dtype=float) @ w
    return weighted + b
