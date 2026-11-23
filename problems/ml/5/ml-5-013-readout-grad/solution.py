import numpy as np


def readout_grad(h, G):
    return np.asarray(h).T @ G
