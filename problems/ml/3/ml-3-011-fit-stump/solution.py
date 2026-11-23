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


def stump(x, y):
    x, y = np.asarray(x), np.asarray(y)
    t = best_cut(x, y)
    return np.array([t, np.mean(y[x <= t]) > 0.5, np.mean(y[x > t]) > 0.5])
