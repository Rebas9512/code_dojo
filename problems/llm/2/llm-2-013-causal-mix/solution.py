import torch


def causal_mix(q, k, v):
    q, k, v = [torch.tensor(a, dtype=torch.float32) for a in (q, k, v)]
    scores = q @ k.T / q.shape[-1] ** 0.5
    future = torch.triu(torch.ones_like(scores, dtype=torch.bool), diagonal=1)
    scores = scores.masked_fill(future, float("-inf"))
    return torch.softmax(scores, dim=-1) @ v
