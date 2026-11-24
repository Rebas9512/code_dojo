import torch


def ledger(a, b):
    x = torch.tensor(1.0, requires_grad=True)
    (a * x).backward()
    first = x.grad.item()
    (b * x).backward()
    return [first, x.grad.item()]
