import numpy as np


def layout(rows):
    grid = np.array(rows)
    return [grid.ndim, grid.shape[0], grid.shape[1]]
