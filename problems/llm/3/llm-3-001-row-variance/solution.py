import torch
x = torch.tensor([[0., 4.], [3., 3.]])
print(torch.var(x, dim=-1, correction=0).tolist())
