import numpy as np


def fees(weights, limit):
    return np.where(np.array(weights) <= limit, 3, 8)
