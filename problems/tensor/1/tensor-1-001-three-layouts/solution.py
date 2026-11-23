import torch
print(tuple(torch.tensor(4).shape))
print(tuple(torch.tensor([4]).shape))
row = torch.tensor([[4, 9]], dtype=torch.float32)
print(tuple(row.shape), row.ndim, row.dtype)
