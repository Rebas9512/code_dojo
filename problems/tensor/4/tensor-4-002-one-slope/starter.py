import torch


def slope(value):
    x = torch.tensor(value, dtype=torch.float32, requires_grad=True)
    loss = x * x
    ____
    return x.grad
