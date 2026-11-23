import torch
import torch.nn as nn


def calibrated(weights, bias):
    w = torch.tensor(weights, dtype=torch.float32)
    b = torch.tensor(bias, dtype=torch.float32)
    torch.manual_seed(0)
    layer = nn.Linear(w.shape[1], w.shape[0])
    with torch.no_grad():
        layer.weight.copy_(w)
        layer.bias.copy_(b)
    return layer
