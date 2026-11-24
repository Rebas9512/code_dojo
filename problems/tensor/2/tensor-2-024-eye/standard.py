import torch


def eye(n):
    i = torch.arange(n)
    return (i[:, None] == i) * 1
