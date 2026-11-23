import numpy as np


def fares(distances, rates):
    d = np.array(distances).reshape(-1, 1)
    return d * np.array(rates)
