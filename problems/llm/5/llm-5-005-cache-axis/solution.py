import torch
past = torch.zeros(2, 3, 2, 4)
fresh = torch.ones(2, 3, 2, 4)
print(tuple(torch.cat([past, fresh], dim=2).shape))
