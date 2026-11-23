import torch
x = torch.tensor([2., 4.])
a = x - torch.mean(x)
middle = x + a
print(middle.tolist())
print((middle + (middle - torch.mean(middle))).tolist())
