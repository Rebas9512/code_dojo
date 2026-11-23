import torch


def gaps(starts, ends):
    a = torch.tensor(starts).unsqueeze(1)
    b = torch.tensor(ends)
    return b - a
