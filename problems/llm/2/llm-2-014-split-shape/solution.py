import torch
x = torch.zeros(2, 3, 8).reshape(2, 3, 4, 2)
print(tuple(x.shape))
print(tuple(x.transpose(1, 2).shape))
