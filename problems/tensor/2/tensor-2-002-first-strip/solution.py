import torch


def first_strip(rows):
    return torch.tensor(rows)[:, 0:1]
