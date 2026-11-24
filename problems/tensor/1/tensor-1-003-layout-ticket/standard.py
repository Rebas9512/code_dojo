import torch


def ticket(rows):
    x = torch.tensor(rows)
    return [x.ndim, x.shape[0], x.shape[1]]
