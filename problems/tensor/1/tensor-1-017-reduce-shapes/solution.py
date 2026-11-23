import torch
x = torch.arange(24).reshape(2, 3, 4)
print(tuple(x.shape))
y = torch.sum(x, dim=1, keepdim=True)
print(tuple(y.shape))
print(tuple(torch.sum(y, dim=2).shape))
