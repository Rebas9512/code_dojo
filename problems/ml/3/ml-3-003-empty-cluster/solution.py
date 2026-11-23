import numpy as np


def relocate(points, labels, centers):
    points = np.asarray(points, dtype=float)
    labels = np.asarray(labels)
    result = np.array(centers, dtype=float)
    for i in range(len(result)):
        members = points[labels == i]
        if len(members):
            result[i] = np.mean(members, axis=0)
    return result
