import numpy as np


def probabilities(scores):
    scores = np.asarray(scores, dtype=float)
    shifted = scores - ...  # 补全这里
    e = np.exp(shifted)
    return e / np.sum(e, axis=1, keepdims=True)
