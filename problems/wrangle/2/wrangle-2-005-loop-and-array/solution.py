import numpy as np
x = np.array([2, 0, 4])
by_hand = [v * 3 + 1 for v in x]
by_array = x * 3 + 1
print(np.array_equal(by_hand, by_array))
