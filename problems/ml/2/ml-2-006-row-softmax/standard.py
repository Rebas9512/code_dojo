import numpy as np


def probabilities(scores):
    scores = np.asarray(scores, dtype=float)
    shifted = scores - np.max(scores, axis=1, keepdims=True)
    weights = np.exp(shifted)
    return weights / np.sum(weights, axis=1, keepdims=True)
