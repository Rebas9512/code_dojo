import numpy as np
import numpy.linalg as la


def fit(X, y):
    A = np.column_stack((X, np.ones(len(X))))
    return la.solve(A.T @ A, A.T @ y)
