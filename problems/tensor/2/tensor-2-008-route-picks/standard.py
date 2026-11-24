import torch


def picks(rows, positions):
    x = torch.tensor(rows)
    columns = torch.tensor(positions)
    return torch.gather(x, 1, columns)
