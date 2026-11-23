import numpy as np


def trace(w, target, rate, steps):
    w = np.asarray(w, dtype=float)
    losses = []
    for _ in range(steps):
        losses.append(float((w - target) ** 2))
        w = w - rate * 2 * (w - target)
    return losses
