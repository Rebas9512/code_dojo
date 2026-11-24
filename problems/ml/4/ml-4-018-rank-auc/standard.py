import numpy as np


def auc(scores, labels):
    order = np.argsort(scores, kind="stable")
    scores, labels = np.asarray(scores)[order], np.asarray(labels)[order]
    wins = 0.0
    earlier_negative = 0
    i = 0
    while i < len(scores):
        j = i + 1
        while j < len(scores) and scores[j] == scores[i]:
            j += 1
        positive = int(np.sum(labels[i:j]))
        negative = j - i - positive
        wins += positive * (earlier_negative + 0.5 * negative)
        earlier_negative += negative
        i = j
    return wins / (np.sum(labels) * earlier_negative)
