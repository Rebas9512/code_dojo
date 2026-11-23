import numpy as np


def assign(points, centers):
    points = np.asarray(points, dtype=float)
    centers = np.asarray(centers, dtype=float)
    distances = np.sum((points[:, None, :] - centers) ** 2, axis=2)
    return ...  # 补全这里
