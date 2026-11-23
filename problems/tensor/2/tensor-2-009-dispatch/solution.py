import torch


def dispatch(rows, positions, updates):
    x = torch.tensor(rows)
    i = torch.tensor(positions)
    return torch.scatter(x, 1, i, torch.tensor(updates))
