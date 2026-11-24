import numpy as np


def transform(train, test):
    center = np.mean(train, axis=0)
    scale = np.std(train, axis=0)
    return (np.asarray(test) - center) / np.where(scale == 0, 1, scale)
