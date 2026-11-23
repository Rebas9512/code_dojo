import torch


def combined(value):
    x = torch.tensor(value, dtype=torch.float32, requires_grad=True)
    (x * x).backward()
    ____
    return x.grad
