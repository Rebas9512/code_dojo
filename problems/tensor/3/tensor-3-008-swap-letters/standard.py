import torch


def swap(a):
    return torch.einsum("ij->ji", a)
