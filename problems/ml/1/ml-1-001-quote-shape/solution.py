import numpy as np
orders = np.array([[1, 2], [0, 3], [2, 1]])
quote = orders @ [2, 1] + 4
print(quote.shape)
print(quote.tolist())
