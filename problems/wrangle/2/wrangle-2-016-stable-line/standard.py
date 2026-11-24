import numpy as np


def queue(scores, names):
    positions = np.argsort(scores, kind='stable')
    return np.array(names)[positions].tolist()
