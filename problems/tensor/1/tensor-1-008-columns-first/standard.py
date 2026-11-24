import torch


def by_column(rows):
    return torch.tensor(rows).transpose(0, 1)
