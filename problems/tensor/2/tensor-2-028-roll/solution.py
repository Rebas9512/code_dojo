import torch


def roll(x, shift):
    i = torch.arange(len(x))
    return x[(i - shift) % len(x)]
