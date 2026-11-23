import torch


def winner_flags(main, spare):
    a = torch.tensor(main)
    b = torch.tensor(spare)
    scores = torch.where(a >= 0, a, b)
    winner = torch.argmax(scores, dim=1)
    return (winner[:, None] == torch.arange(a.shape[1])) * 1
