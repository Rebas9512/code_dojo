import torch


def step_reading(value):
    x = torch.tensor(value, dtype=torch.float32, requires_grad=True)
    loss = x * x
    loss.backward()
    with torch.no_grad():
        x.add_(1)
    return [x.item(), x.grad.item()]
