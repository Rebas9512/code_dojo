import torch


def triu(x):
    r = torch.arange(x.shape[0])[:, None]
    c = torch.arange(x.shape[1])
    return x * (c >= r)
