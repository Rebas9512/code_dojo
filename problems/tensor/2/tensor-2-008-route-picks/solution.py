import torch


def picks(rows, positions):
    x = torch.tensor(rows)
    i = torch.tensor(positions)
    return torch.gather(x, 1, i)
