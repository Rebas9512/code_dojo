import torch


def preview(x):
    with torch.no_grad():
        value = x + 1
    return value
