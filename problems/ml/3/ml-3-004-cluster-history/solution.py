import numpy as np


def cluster(points, centers, rounds):
    points = np.asarray(points, dtype=float)
    centers = np.asarray(centers, dtype=float)
    history = []
    for _ in range(rounds):
        distance = np.sum((points[:, None, :] - centers) ** 2, axis=2)
        labels = np.argmin(distance, axis=1)
        updated = centers.copy()
        for i in range(len(centers)):
            members = points[labels == i]
            if len(members):
                updated[i] = np.mean(members, axis=0)
        history.append((updated, labels))
        centers = updated
    return history
