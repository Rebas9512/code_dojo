import torch


def count_parameters(layer):
    count = 0
    for p in layer.parameters():
        count += p.numel()
    return count
