import numpy as np


def class_loss(X, W, b, y):
    scores = np.asarray(X, dtype=float) @ W + b
    scores = scores - np.max(scores, axis=1, keepdims=True)
    normalizer = np.log(np.sum(np.exp(scores), axis=1))
    return np.mean(normalizer - scores[np.arange(len(y)), y])
