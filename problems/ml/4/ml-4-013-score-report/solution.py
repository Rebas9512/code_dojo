import numpy as np


def ratio(a, b):
    return float(a / b) if b else 0.0


def scores(cm):
    (tn, fp), (fn, tp) = np.asarray(cm)
    return [ratio(tn + tp, tn + fp + fn + tp), ratio(tp, tp + fp),
            ratio(tp, tp + fn), ratio(2 * tp, 2 * tp + fp + fn)]
