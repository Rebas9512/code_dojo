import torch
p = torch.tensor(3., requires_grad=True)
loss = p * 2
print(type(loss.item()).__name__, loss.requires_grad)
