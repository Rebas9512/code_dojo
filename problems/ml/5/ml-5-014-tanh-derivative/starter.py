import numpy as np


def hidden_grad(Z, W2, G):
    h = np.tanh(Z)
    upstream = np.asarray(G) @ np.asarray(W2).T
    return upstream * (1 - h)
