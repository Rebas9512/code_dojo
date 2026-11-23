import numpy as np
from dojo_grad import check_grad

def check_function(args, expected, backward):
    x, upstream = (np.asarray(a, dtype=float) for a in args)
    def objective(t):
        weights = np.exp(t - t.max())
        return (weights / weights.sum()) @ upstream

    return check_grad(lambda t: backward(t, upstream), objective, [x])
