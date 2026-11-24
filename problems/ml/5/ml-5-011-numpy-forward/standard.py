import numpy as np


def forward(X, W1, b1, W2, b2):
    h = np.tanh(np.asarray(X, dtype=float) @ W1 + b1)
    return h @ W2 + b2
