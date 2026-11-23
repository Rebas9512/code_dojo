import torch
x = torch.tensor([1., 2.], requires_grad=True)
g = torch.tensor([3., -1.])
torch.sum(x * x * g).backward()
print(x.grad.tolist())
