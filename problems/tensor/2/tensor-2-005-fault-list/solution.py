import torch


def faults(rows):
    x = torch.tensor(rows)
    return x[x < 0].tolist()
