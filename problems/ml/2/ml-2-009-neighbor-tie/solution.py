import numpy as np
x = np.array([5, 1, 3, 9])
print(np.argsort((x - 3) ** 2, kind="stable")[:2].tolist())
