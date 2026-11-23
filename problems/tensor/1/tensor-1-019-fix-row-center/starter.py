import torch


def center(rows):
    x = torch.tensor(rows, dtype=torch.float32)
    m = torch.mean(x, dim=1)
    return x - m
