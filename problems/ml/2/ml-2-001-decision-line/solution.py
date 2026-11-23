import numpy as np
points = np.array([[0, 1], [2, 0], [2, 1]])
score = points @ [1, 1] - 2
print(score.tolist())
print((score >= 0).astype(int).tolist())
