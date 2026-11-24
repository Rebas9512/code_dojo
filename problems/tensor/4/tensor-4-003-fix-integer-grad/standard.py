import torch


def cube_slopes(values):
    x = torch.tensor(values, dtype=torch.float32, requires_grad=True)
    torch.sum(x**3).backward()
    return x.grad
