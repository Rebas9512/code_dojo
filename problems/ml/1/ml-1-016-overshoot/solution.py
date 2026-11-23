import numpy as np
w = np.array(2.)
for _ in range(2):
    print(float(w ** 2))
    w -= 1.5 * 2 * w
