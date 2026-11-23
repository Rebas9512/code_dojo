import torch


def multi_mix(q, k, v, heads):
    batch, length, width = torch.tensor(q).shape
    depth = width // heads
    q, k, v = [torch.tensor(a, dtype=torch.float32).reshape(
        batch, length, heads, depth).transpose(1, 2) for a in (q, k, v)]
    scores = q @ k.transpose(-2, -1) / depth ** 0.5
    future = torch.triu(torch.ones(length, length, dtype=torch.bool), diagonal=1)
    mixed = torch.softmax(scores.masked_fill(future, float("-inf")), dim=-1) @ v
    return mixed.transpose(1, 2).reshape(batch, length, width)
