import torch


def recipes(a, b):
    return torch.einsum("ij,jk->ik", a, b)
