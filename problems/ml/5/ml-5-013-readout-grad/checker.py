import numpy as np
from dojo_grad import check_grad


def check_function(args, expected, readout_grad):
    h, G = [np.asarray(a, dtype=float) for a in args]
    W = np.zeros((h.shape[1], G.shape[1]))
    return check_grad(lambda w: readout_grad(h, G), lambda w: np.sum((h @ w) * G), [W])
