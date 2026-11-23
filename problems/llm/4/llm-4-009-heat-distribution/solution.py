import torch


def distributions(scores, temperature):
    z = torch.tensor(scores, dtype=torch.float32)
    return torch.softmax(z / temperature, dim=-1)
