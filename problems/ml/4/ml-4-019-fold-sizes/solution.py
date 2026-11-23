import numpy as np
blocks = np.array_split(np.arange(7), 3)
print([len(block) for block in blocks])
