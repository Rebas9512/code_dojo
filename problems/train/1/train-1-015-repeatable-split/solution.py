import torch


def split_ids(n, count, seed):
    g = torch.Generator().manual_seed(seed)
    ids = torch.randperm(n, generator=g).tolist()
    return [ids[count:], ids[:count]]
