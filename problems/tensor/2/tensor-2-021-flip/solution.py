import torch


def flip(x):
    i = torch.arange(len(x))
    return x[len(x) - 1 - i]
