import torch


def dispatch(rows, positions, updates):
    x = torch.tensor(rows)
    columns = torch.tensor(positions)
    return torch.scatter(x, 1, columns, torch.tensor(updates))
