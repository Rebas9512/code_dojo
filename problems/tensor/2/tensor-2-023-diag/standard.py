import torch


def diag(x):
    rows, cols = x.shape
    i = torch.arange(rows)
    i = i[i < cols]
    return x[i, i]
