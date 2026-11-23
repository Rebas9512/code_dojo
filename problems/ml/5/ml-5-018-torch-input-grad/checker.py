import numpy as np
from dojo_grad import check_grad


def check_function(args, expected, input_grad):
    X, W1, b1, W2, b2, G = [np.asarray(a, dtype=float) for a in args]
    def objective(x):
        return np.sum((np.tanh(x @ W1 + b1) @ W2 + b2) * G)
    return check_grad(lambda x: input_grad(x.tolist(), *args[1:]), objective, [X])
