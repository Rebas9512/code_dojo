import torch
x = torch.arange(12).reshape(3, 4)
print(tuple(x[:, 1].shape))
print(tuple(x[:, 1:2].shape))
print(tuple(x[1:, ::2].shape))
