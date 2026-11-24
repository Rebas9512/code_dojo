import numpy as np


def classify(X, W, b):
    scores = np.asarray(X, dtype=float) @ W + b
    shifted = scores - np.max(scores, axis=1, keepdims=True)
    weights = np.exp(shifted)
    return weights / np.sum(weights, axis=1, keepdims=True)
