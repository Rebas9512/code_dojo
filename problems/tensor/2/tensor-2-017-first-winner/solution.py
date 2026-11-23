import torch


def winners(rows):
    return torch.argmax(torch.tensor(rows), dim=1)
