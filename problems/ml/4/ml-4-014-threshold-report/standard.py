import numpy as np


def threshold_report(z, y, levels):
    prob = np.exp(-np.logaddexp(0, -np.asarray(z, dtype=float)))
    y = np.asarray(y)
    actual = np.sum(y)
    rows = []
    for level in levels:
        pred = prob >= level
        tp = np.sum(y[pred])
        reported = np.sum(pred)
        precision = tp / reported if reported else 0.0
        recall = tp / actual if actual else 0.0
        rows.append([precision, recall])
    return rows
