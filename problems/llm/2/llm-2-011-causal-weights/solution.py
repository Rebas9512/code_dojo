import torch


def causal_weights(scores):
    scores = torch.tensor(scores, dtype=torch.float32)
    length = scores.shape[-1]
    future = torch.triu(torch.ones(length, length, dtype=torch.bool), diagonal=1)
    return torch.softmax(scores.masked_fill(future, float("-inf")), dim=-1)
