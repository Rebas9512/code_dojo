import torch
import torch.nn as nn


def initial_offsets(width, start):
    values = torch.full((width,), float(start))
    return nn.Parameter(values)
