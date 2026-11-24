import torch


def bills(a, p):
    return torch.einsum("ij,j->i", a, p)
