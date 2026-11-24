import torch


def position_slice(pos, start, length):
    return torch.tensor(pos[start:start + length], dtype=torch.float32)
