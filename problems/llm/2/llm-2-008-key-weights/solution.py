import torch


def attention_weights(q, k):
    q = torch.tensor(q, dtype=torch.float32)
    k = torch.tensor(k, dtype=torch.float32)
    scores = q @ k.T / k.shape[-1] ** 0.5
    return torch.softmax(scores, dim=-1)
