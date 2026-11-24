import torch


def shift(rows, bias):
    readings = torch.tensor(rows)
    row_bias = torch.tensor(bias).unsqueeze(1)
    return readings + row_bias
