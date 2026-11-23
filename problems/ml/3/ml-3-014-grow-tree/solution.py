import numpy as np


def best_cut(x, y):
    values = np.unique(x)
    best_score = np.inf
    threshold = 0.0
    for t in (values[:-1] + values[1:]) / 2:
        mask = x <= t
        score = 0.0
        for group in (y[mask], y[np.logical_not(mask)]):
            p = np.mean(group)
            score += len(group) * 2 * p * (1 - p)
        if score < best_score - 1e-12:
            threshold, best_score = t, score
    return threshold


def grow(x, y, depth):
    x, y = np.asarray(x), np.asarray(y)
    if depth == 0 or len(np.unique(x)) == 1 or len(np.unique(y)) == 1:
        return [[0.0, float(np.mean(y) > 0.5)]]
    t = best_cut(x, y)
    left = x <= t
    return [[1.0, float(t)]] + grow(x[left], y[left], depth - 1) + grow(x[x > t], y[x > t], depth - 1)
