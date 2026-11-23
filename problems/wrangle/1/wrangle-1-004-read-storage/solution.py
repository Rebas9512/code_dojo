import numpy as np


def reading_type(values):
    a = np.array(values, dtype=float)
    return [a.shape[0], str(a.dtype)]
