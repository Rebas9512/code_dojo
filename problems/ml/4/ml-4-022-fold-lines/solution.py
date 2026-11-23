import numpy as np
import numpy.linalg as la


def validate_line(x, y, k):
    A = np.column_stack((x, np.ones(len(x))))
    y = np.asarray(y, dtype=float)
    result = []
    for ids in np.array_split(np.arange(len(x)), k):
        train = np.ones(len(x), dtype=bool)
        train[ids] = False
        design = A[train]
        params = la.solve(design.T @ design, design.T @ y[train])
        result.append(np.mean((A[ids] @ params - y[ids]) ** 2))
    return result
