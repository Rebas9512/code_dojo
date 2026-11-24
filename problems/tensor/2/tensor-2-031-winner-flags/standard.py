import torch


def winner_flags(main, spare):
    primary = torch.tensor(main)
    scores = torch.where(primary >= 0, primary, torch.tensor(spare))
    winner = torch.argmax(scores, dim=1)
    return (winner[:, None] == torch.arange(scores.shape[1])) * 1
