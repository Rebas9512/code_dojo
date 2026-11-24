import numpy as np


def reading_type(values):
    readings = np.array(values, dtype=float)
    return [readings.shape[0], str(readings.dtype)]
