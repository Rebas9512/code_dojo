import numpy as np
from dojo_grad import check_grad


def check_function(args, expected, sensitivity):
    def backward(x, w, b):
        return sensitivity(float(x), float(w), float(b))

    return check_grad(backward, lambda x, w, b: np.tanh(x*w + b),
                      [np.array(v, dtype=float) for v in args])
