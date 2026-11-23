import torch
a = torch.arange(2).unsqueeze(1)
b = torch.arange(4).unsqueeze(0)
print(tuple(a.shape))
print(tuple(b.shape))
print(tuple((a + b).shape))
