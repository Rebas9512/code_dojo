import numpy as np
from dojo_grad import check_grad


def check_function(args, expected, hidden_grad):
    Z, W2, G = [np.asarray(a, dtype=float) for a in args]

    def objective(z):
        return np.sum((np.tanh(z) @ W2) * G)

    return check_grad(lambda z: hidden_grad(z, W2, G), objective, [Z])
