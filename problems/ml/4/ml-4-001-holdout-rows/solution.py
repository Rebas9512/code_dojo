import numpy as np
order = np.random.default_rng(0).permutation(4)
print(order[:2].tolist())
print(order[2:].tolist())
