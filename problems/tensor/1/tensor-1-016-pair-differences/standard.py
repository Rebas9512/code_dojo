import torch


def gaps(starts, ends):
    start_column = torch.tensor(starts).unsqueeze(1)
    return torch.tensor(ends) - start_column
