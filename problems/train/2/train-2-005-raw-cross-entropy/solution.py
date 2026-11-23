import torch


def class_loss(rows, ids):
    scores = torch.tensor(rows, dtype=torch.float64)
    labels = torch.tensor(ids, dtype=torch.long)
    return torch.nn.CrossEntropyLoss()(scores, labels).item()
