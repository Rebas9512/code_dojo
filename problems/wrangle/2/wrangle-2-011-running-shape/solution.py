import numpy as np
a = np.array([[2, 5, 1], [0, 1, 3]])
print(np.cumsum(a, axis=1).shape)
