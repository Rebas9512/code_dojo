import numpy as np
x = np.array([4, 5, 8])
print(np.where(x >= 5, 1, 0).tolist())
