import torch
z = torch.tensor([3., 5., 3., 0.])
print(torch.argsort(z, descending=True, stable=True)[:2].tolist())
