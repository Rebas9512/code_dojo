import torch


def cube_slopes(values):
    x = torch.tensor(values, requires_grad=True)
    torch.sum(x ** 3).backward()
    return x.grad
