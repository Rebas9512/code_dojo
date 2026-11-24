import numpy as np


def gradients(X, W1, b1, W2, b2, G):
    X, W1 = np.asarray(X), np.asarray(W1)
    W2, G = np.asarray(W2), np.asarray(G)
    h = np.tanh(X @ W1 + b1)
    dz = (G @ W2.T) * (1 - h ** 2)

    dX = dz @ W1.T
    dW1 = X.T @ dz
    db1 = np.sum(dz, axis=0)
    dW2 = h.T @ G
    db2 = np.sum(G, axis=0)
    return dX, dW1, db1, dW2, db2
