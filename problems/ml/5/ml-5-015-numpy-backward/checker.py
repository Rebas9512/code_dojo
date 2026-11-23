import numpy as np
from dojo_grad import check_grad


def check_function(args, expected, gradients):
    X, W1, b1, W2, b2, G = [np.asarray(a, dtype=float) for a in args]

    def objective(x, w, b, v, c):
        return np.sum((np.tanh(x @ w + b) @ v + c) * G)

    def backward(x, w, b, v, c):
        return gradients(x, w, b, v, c, G)

    return check_grad(backward, objective, [X, W1, b1, W2, b2])
