import numpy as np
cm = np.array([[5, 3], [0, 1]])
print(float(cm[1, 1] / np.sum(cm[:, 1])))
