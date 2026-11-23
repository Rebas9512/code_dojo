import torch


def backup(main, spare):
    x = torch.tensor(main)
    y = torch.tensor(spare)
    return torch.where(x >= 0, x, y)
