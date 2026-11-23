import torch

def attention(q, k, v):
    q, k, v = (torch.tensor(matrix) for matrix in (q, k, v))
    weights = (q @ k.T / k.shape[1] ** 0.5).softmax(dim=-1)
    return weights @ v
