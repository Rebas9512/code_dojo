import torch
x = torch.arange(3).unsqueeze(0)
print(tuple(x.shape))
x = x.unsqueeze(2)
print(tuple(x.shape))
print(tuple(x.squeeze(2).shape))
