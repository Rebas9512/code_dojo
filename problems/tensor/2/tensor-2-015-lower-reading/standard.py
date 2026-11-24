import torch


def lower(left, right):
    a = torch.tensor(left)
    b = torch.tensor(right)
    return torch.where(a <= b, a, b)
