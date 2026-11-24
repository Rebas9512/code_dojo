import torch


def logits(hidden, readout):
    x = torch.tensor(hidden, dtype=torch.float32)
    w = torch.tensor(readout, dtype=torch.float32)
    return x @ w.T
