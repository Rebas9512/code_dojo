import torch


def totals(rows):
    return torch.sum(torch.tensor(rows), dim=0)
