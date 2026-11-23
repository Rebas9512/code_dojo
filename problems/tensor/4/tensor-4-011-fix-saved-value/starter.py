import torch


def step_reading(value):
    x = torch.tensor(value, dtype=torch.float32, requires_grad=True)
    loss = x * x
    with torch.no_grad():
        x.add_(1)
    loss.backward()
    return [x.item(), x.grad.item()]
