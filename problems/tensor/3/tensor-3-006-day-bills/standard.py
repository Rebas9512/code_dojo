import torch


def day_bills(a, p):
    return torch.einsum("bij,bj->bi", a, p)
