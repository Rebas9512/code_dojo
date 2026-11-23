import torch
from torch.utils.data import DataLoader


def shuffled(values, width, seed):
    generator = torch.Generator().manual_seed(seed)
    return DataLoader(values, batch_size=width, shuffle=True, generator=generator)
