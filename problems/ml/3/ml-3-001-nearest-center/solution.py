import numpy as np
x = np.array([1, 4, 8])
c = np.array([1, 1, 7])
print(np.argmin((x[:, None] - c) ** 2, axis=1).tolist())
