import torch


def positioned(weight, pos, ids, start):
    table = torch.tensor(weight, dtype=torch.float32)
    vectors = table[torch.tensor(ids)]
    length = vectors.shape[1]
    positions = torch.tensor(pos[start:start + length], dtype=torch.float32)
    return vectors + positions
