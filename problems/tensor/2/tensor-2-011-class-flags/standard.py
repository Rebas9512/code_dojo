import torch


def flags(labels, classes):
    rows = torch.tensor(labels).unsqueeze(1)
    return rows == torch.arange(classes)
