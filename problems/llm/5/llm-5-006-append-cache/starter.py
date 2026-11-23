import torch


def append_cache(past, fresh):
    old = torch.tensor(past, dtype=torch.float32)
    new = torch.tensor(fresh, dtype=torch.float32)
    return ...
