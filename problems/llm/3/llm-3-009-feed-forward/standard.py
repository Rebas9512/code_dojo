import torch
import torch.nn.functional as F


def feed_forward(x, up, down):
    x, up, down = [torch.tensor(a, dtype=torch.float32) for a in (x, up, down)]
    expanded = F.linear(x, up)
    return F.linear(F.gelu(expanded), down)
