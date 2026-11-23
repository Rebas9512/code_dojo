import torch
scores = torch.tensor([[8, 0, 1], [-1, 3, 3]])
print(torch.argmax(scores[-1]).item())
