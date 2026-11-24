import torch


def triu(x):
    row = torch.arange(x.shape[0])[:, None]
    column = torch.arange(x.shape[1])
    return x * (column >= row)
