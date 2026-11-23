import torch


def shares(rows):
    x = torch.tensor(rows)
    return x / torch.sum(x, dim=1, keepdim=True)
