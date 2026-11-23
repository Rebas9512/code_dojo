import numpy as np


def probabilities(scores):
    scores = np.asarray(scores, dtype=float)
    shifted = scores - np.max(scores, axis=1, keepdims=True)
    e = np.exp(shifted)
    return e / np.sum(e, axis=1, keepdims=True)
