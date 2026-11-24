import torch


def vstack(a, b):
    row = torch.arange(2)[:, None]
    return (row == 0) * a + (row == 1) * b
