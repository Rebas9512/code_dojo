import torch
import torch.nn as nn


class GainMeter(nn.Module):
    def __init__(self, gains):
        nn.Module.__init__(self)
        self.gain = nn.Parameter(torch.tensor(gains, dtype=torch.float32))

    def forward(self, x):
        return x * self.gain

    def record(self, x):
        # 共用本层的前向公式，逐笔累计通道贡献。
        loss = torch.sum(self.forward(x))
        loss.backward()


def make_meter(gains):
    return GainMeter(gains)
