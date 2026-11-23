import torch


def positioned(weight, pos, ids, start):
    vectors = torch.tensor(weight, dtype=torch.float32)[torch.tensor(ids)]
    positions = torch.tensor(pos, dtype=torch.float32)
    return vectors + positions[start:start + vectors.shape[1]]
