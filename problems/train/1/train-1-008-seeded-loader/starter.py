import torch
from torch.utils.data import DataLoader


def shuffled(values, width, seed):
    generator = torch.Generator().manual_seed(seed)
    ____  # 在此补全
