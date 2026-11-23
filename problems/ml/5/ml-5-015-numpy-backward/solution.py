import numpy as np


def gradients(X, W1, b1, W2, b2, G):
    X, W1, W2, G = np.asarray(X), np.asarray(W1), np.asarray(W2), np.asarray(G)
    h = np.tanh(X @ W1 + b1)
    dz = (G @ W2.T) * (1 - h ** 2)
    return dz @ W1.T, X.T @ dz, np.sum(dz, axis=0), h.T @ G, np.sum(G, axis=0)
