import torch
import torch.nn as nn


class ChannelAffine(nn.Module):
    def __init__(self, gain, offset):
        nn.Module.__init__(self)
        self.gain = nn.Parameter(torch.tensor(gain, dtype=torch.float32))
        self.offset = nn.Parameter(torch.tensor(offset, dtype=torch.float32))

    def forward(self, x):
        return x * self.gain + self.offset


def make_affine(gain, offset):
    return ChannelAffine(gain, offset)
