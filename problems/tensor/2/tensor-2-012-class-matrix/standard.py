import torch


def encode(labels, classes):
    indices = torch.tensor(labels).unsqueeze(1)
    base = torch.zeros((len(labels), classes), dtype=torch.int64)
    return torch.scatter(base, 1, indices, 1)
