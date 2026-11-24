import numpy as np


def inertia(points, centers):
    points = np.asarray(points, dtype=float)
    centers = np.asarray(centers, dtype=float)
    distances = np.sum((points[:, None, :] - centers) ** 2, axis=2)
    labels = np.argmin(distances, axis=1)
    total = 0.0
    for i in range(len(centers)):
        members = points[labels == i]
        if len(members):
            center = np.mean(members, axis=0)
            total += np.sum((members - center) ** 2)
    return total
