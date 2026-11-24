import torch.nn as nn


def readout(inputs, outputs):
    return nn.Linear(inputs, outputs, bias=False)
