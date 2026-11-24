import torch


def combined(value):
    x = torch.tensor(value, dtype=torch.float32, requires_grad=True)
    (x * x).backward()
    (3 * x).backward()
    return x.grad
