import torch


def column_strip(rows):
    x = torch.tensor(rows).transpose(0, 1)
    return x.view(-1)
