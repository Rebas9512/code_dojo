import torch


def greedy_id(scores):
    last = torch.tensor(scores[-1])
    return torch.argmax(last).item()
