import torch
q = torch.zeros(2, 4)
k = torch.ones(3, 4)
print(tuple((q @ k.T).shape))
