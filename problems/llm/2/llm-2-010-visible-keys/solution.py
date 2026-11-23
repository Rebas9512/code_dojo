import torch
future = torch.triu(torch.ones(4, 4, dtype=torch.bool), diagonal=1)
print(future[1].tolist())
