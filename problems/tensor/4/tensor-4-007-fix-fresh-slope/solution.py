import torch


def fresh(value):
    x = torch.tensor(value, dtype=torch.float32, requires_grad=True)
    (x * x).backward()
    first = x.grad.item()
    x.grad = None
    (5 * x).backward()
    return [first, x.grad.item()]
