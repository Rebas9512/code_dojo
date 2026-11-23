import numpy as np


def classify(X, W, b):
    scores = np.asarray(X, dtype=float) @ W + b
    shifted = scores - np.max(scores, axis=1, keepdims=True)
    e = np.exp(shifted)
    return e / np.sum(e, axis=1, keepdims=True)
