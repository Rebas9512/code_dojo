import torch
x = torch.arange(12)
print(tuple(x.shape))
x = x.view(3, -1)
print(tuple(x.shape))
print(tuple(x.reshape(2, 2, -1).shape))
