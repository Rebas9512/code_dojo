import torch


def batch_diag(a):
    return torch.einsum("bii->bi", a)
