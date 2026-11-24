import torch


def scores(rows, k):
    return torch.topk(torch.tensor(rows), k, dim=1).values
