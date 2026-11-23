import torch


def add_update(values, update):
    x = torch.tensor(values, dtype=torch.float32)
    delta = torch.tensor(update, dtype=torch.float32)
    return ...
