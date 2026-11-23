import torch
x = torch.tensor([[5, 8, 2], [4, 1, 9]])
idx = torch.tensor([[2, 0], [1, 1]])
print(torch.gather(x, 1, idx).tolist())
print(tuple(torch.scatter(x, 1, idx, 0).shape))
