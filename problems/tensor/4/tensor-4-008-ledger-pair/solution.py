import torch


def ledger(a, b):
    x = torch.tensor(1., requires_grad=True)
    (a * x).backward()
    first = x.grad.clone()
    (b * x).backward()
    return [first.item(), x.grad.item()]
