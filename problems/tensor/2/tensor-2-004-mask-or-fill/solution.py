import torch
x = torch.tensor([[-1, 3, 0], [2, -5, 1]])
bad = x < 0
print(tuple(bad.shape))
print(tuple(x[bad].shape))
print(tuple(x.masked_fill(bad, 0).shape))
