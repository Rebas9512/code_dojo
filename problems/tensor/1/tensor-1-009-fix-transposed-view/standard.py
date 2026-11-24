import torch


def column_strip(rows):
    columns = torch.tensor(rows).transpose(0, 1)
    return columns.reshape(-1)
