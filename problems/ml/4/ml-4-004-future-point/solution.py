import numpy as np
train = np.array([2., 6.])
test = np.array([8., 12.])
print(((test - np.mean(train)) / np.std(train)).tolist())
