import torch


def weights(a, b):
    return torch.einsum("i,j->ij", a, b)
