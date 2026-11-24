import torch


def two_skips(values, a, b):
    x = torch.tensor(values, dtype=torch.float32)
    middle = x + a * x
    return middle + b * middle
