import numpy as np


def threshold_report(z, y, levels):
    prob = np.exp(-np.logaddexp(0, -np.asarray(z, dtype=float)))
    y = np.asarray(y)
    rows = []
    for level in levels:
        pred = prob >= level
        tp = np.sum(y[pred])
        reported, actual = np.sum(pred), np.sum(y)
        rows.append([tp / reported if reported else 0.0, tp / actual if actual else 0.0])
    return rows
