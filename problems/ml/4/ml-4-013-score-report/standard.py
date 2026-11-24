import numpy as np


def ratio(numerator, denominator):
    return numerator / denominator if denominator else 0.0


def scores(cm):
    (tn, fp), (fn, tp) = np.asarray(cm)
    total = tn + fp + fn + tp
    return [
        (tn + tp) / total,
        ratio(tp, tp + fp),
        ratio(tp, tp + fn),
        ratio(2 * tp, 2 * tp + fp + fn),
    ]
