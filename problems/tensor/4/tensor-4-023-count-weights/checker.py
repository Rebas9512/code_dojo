import torch
from torch import nn


def check_function(args, expected, fn):
    torch.manual_seed(0)
    layer = nn.Linear(*args)
    return fn(layer) == expected
