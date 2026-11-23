import torch


def unroll(rows):
    return torch.tensor(rows).reshape(-1)
