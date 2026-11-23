import numpy as np
q = np.array([0., 1., 2., 1.5])
print(np.where(q <= 0.5, 0, np.where(q <= 1.5, 1, 0)).tolist())
