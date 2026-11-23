import numpy as np
X = np.ones((3, 2))
h = np.tanh(X @ np.ones((2, 4)))
print(h.shape)
print((h @ np.ones((4, 1))).shape)
