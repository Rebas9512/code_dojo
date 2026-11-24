import torch
import torch.nn as nn


class ChannelGain(nn.Module):
    def __init__(self, initial):
        nn.Module.__init__(self)
        self.gain = nn.Parameter(torch.tensor(initial, dtype=torch.float32))

    def forward(self, x):
        return x * self.gain


def make_gain(initial):
    return ChannelGain(initial)
