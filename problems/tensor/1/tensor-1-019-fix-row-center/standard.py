import torch


def center(rows):
    x = torch.tensor(rows, dtype=torch.float32)
    row_mean = torch.mean(x, dim=1, keepdim=True)
    return x - row_mean
