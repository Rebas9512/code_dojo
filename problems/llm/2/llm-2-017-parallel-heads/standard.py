import torch


def multi_mix(q, k, v, heads):
    tensors = [torch.tensor(values, dtype=torch.float32) for values in (q, k, v)]
    batch, length, width = tensors[0].shape
    depth = width // heads
    q, k, v = [
        tensor.reshape(batch, length, heads, depth).transpose(1, 2)
        for tensor in tensors
    ]

    scores = q @ k.transpose(-2, -1) / depth ** 0.5
    future = torch.triu(torch.ones(length, length, dtype=torch.bool), diagonal=1)
    weights = torch.softmax(scores.masked_fill(future, float("-inf")), dim=-1)
    mixed = weights @ v
    return mixed.transpose(1, 2).reshape(batch, length, width)
