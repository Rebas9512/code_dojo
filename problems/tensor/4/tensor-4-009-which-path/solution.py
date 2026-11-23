import torch
x = torch.tensor(4., requires_grad=True)
with torch.no_grad():
    frozen = x + 1
y = x * x.detach()
print(x.requires_grad, frozen.requires_grad, y.requires_grad)
y.backward()
print(x.grad.item())
