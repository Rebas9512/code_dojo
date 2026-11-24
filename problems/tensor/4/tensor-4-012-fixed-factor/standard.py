import torch


def fixed_factor(x):
    return x * x.detach()
