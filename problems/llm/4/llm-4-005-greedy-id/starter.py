import torch


def greedy_id(scores):
    last = torch.tensor(scores)[-1]
    return ...
