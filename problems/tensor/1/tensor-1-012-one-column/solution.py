import torch


def one_column(values):
    return torch.tensor(values).unsqueeze(1)
