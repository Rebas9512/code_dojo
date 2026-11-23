import torch


def backup(main, spare):
    x = torch.tensor(main)
    y = torch.tensor(spare)
    return torch.where(____, x, y)
