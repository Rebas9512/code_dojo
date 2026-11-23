import torch
labels = torch.tensor([1, 1]).unsqueeze(1)
cols = torch.arange(3)
print(tuple(labels.shape))
print((labels == cols).tolist())
