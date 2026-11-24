import torch


def repair(rows, fill):
    x = torch.tensor(rows)
    return x.masked_fill(x < 0, fill)
