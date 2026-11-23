import torch


def energy_grad(x):
    x.requires_grad_(True)
    loss = torch.sum((x - 1) ** 2)
    loss.backward()
    return x.grad
