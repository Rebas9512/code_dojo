import torch
import torch.nn as nn


def readout(inputs, outputs):
    torch.manual_seed(0)
    return nn.Linear(inputs, outputs, bias=False)
