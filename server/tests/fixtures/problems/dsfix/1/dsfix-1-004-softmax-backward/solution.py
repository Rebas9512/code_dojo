import numpy as np

def backward(x, upstream):
    weights = np.exp(x - x.max())
    p = weights / weights.sum()
    return p * (upstream - (p * upstream).sum())
