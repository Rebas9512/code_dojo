import numpy as np
import numpy.linalg as la
A = np.array([[1, 1], [2, 1], [3, 1]])
print((A.T @ A).shape)
print(la.solve(A.T @ A, A.T @ [3, 5, 7]).shape)
