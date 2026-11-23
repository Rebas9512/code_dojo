import torch
x = torch.tensor(2., requires_grad=True)
(x * x).backward()
print(x.grad.item())
(3 * x).backward()
print(x.grad.item())
x.grad = None
(-x).backward()
print(x.grad.item())
