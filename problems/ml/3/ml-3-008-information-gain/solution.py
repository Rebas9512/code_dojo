import numpy as np


def entropy(labels):
    counts = np.bincount(labels)
    p = counts[counts > 0] / len(labels)
    return -np.sum(p * np.log2(p))


def gain(left, right):
    total = len(left) + len(right)
    remaining = (len(left) * entropy(left) + len(right) * entropy(right)) / total
    return entropy(np.concatenate((left, right))) - remaining
