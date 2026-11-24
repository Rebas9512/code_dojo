import numpy as np


def fares(distances, rates):
    distance_column = np.array(distances).reshape(-1, 1)
    return distance_column * np.array(rates)
