import torch


def shift(rows, bias):
    x = torch.tensor(rows)
    d = torch.tensor(bias)
    return x + d.unsqueeze(1)
