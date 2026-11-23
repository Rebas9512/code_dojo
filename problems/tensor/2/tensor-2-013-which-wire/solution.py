import torch
x = torch.tensor([0, -2, 4])
b = torch.tensor([5, 6, 7])
print((x >= 0).tolist())
print(torch.where(x >= 0, x, b).tolist())
