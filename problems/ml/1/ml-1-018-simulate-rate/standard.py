import numpy as np


def trace(w, target, rate, steps):
    w = np.asarray(w, dtype=float)
    losses = []
    for _ in range(steps):
        residual = w - target
        losses.append(float(residual**2))
        w = w - rate * 2 * residual
    return losses
