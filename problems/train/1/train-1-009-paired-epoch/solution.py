import torch
from torch.utils.data import DataLoader


def paired_epoch(values, labels, width, seed):
    pairs = list(zip(values, labels))
    generator = torch.Generator().manual_seed(seed)
    loader = DataLoader(pairs, batch_size=width, shuffle=True, generator=generator)
    return [[xs.tolist(), ys.tolist()] for xs, ys in loader]
