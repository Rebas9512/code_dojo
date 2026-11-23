import numpy as np


def record(weights, target):
    losses = []
    for w in np.asarray(weights, dtype=float):
        losses.append(float((w - target) ** 2))
    return losses
