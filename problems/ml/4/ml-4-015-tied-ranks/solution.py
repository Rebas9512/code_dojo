import numpy as np
positive = np.array([4., 2., 0.])
negative = 2.
print(((positive > negative) + 0.5 * (positive == negative)).tolist())
