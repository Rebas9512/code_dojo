import torch


def rescale(scores, temperature):
    z = torch.tensor(scores, dtype=torch.float32)
    return ...
