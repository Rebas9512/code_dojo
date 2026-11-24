import numpy as np


def roc(scores, labels):
    order = np.argsort(scores)[::-1]
    scores = np.asarray(scores)[order]
    labels = np.asarray(labels)[order]
    positive = int(np.sum(labels))
    negative = len(labels) - positive
    tp, fp = 0, 0
    points = [[0.0, 0.0]]
    for i, label in enumerate(labels):
        tp += int(label == 1)
        fp += int(label == 0)
        if i + 1 == len(labels) or scores[i + 1] != scores[i]:
            points.append([fp / negative, tp / positive])
    return points
