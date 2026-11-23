import torch


def standardize(x, eps):
    x = torch.tensor(x, dtype=torch.float32)
    delta = x - torch.mean(x, dim=-1, keepdim=True)
    variance = ...
    return delta / torch.sqrt(variance + eps)
