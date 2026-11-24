import torch


def logits(q, k):
    return torch.einsum("bqd,bkd->bqk", q, k)
