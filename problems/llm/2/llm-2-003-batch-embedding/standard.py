import torch


def embed_batch(weight, ids):
    table = torch.tensor(weight, dtype=torch.float32)
    return table[torch.tensor(ids)]
