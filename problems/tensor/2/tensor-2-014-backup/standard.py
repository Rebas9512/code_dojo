import torch


def backup(main, spare):
    primary = torch.tensor(main)
    return torch.where(primary >= 0, primary, torch.tensor(spare))
