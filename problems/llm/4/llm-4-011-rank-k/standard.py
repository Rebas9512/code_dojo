import torch


def rank_k(scores, k):
    order = torch.argsort(torch.tensor(scores), descending=True, stable=True)
    return order[:k].tolist()
