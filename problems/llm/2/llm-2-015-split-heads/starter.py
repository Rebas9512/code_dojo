import torch


def split_heads(values, heads):
    x = torch.tensor(values, dtype=torch.float32)
    batch, length, width = x.shape
    groups = x.reshape(batch, length, heads, width // heads)
    return ...
