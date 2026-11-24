import torch


def alternate(rows):
    return torch.tensor(rows)[:, ::2]
