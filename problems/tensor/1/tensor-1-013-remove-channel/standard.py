import torch


def remove_channel(rows):
    return torch.tensor(rows).squeeze(1).transpose(0, 1)
