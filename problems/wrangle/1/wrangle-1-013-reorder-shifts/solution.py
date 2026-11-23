import numpy as np


def shifts(rows, positions, minimum):
    picked = np.array(rows)[positions]
    return picked[picked[:, 0] >= minimum].tolist()
