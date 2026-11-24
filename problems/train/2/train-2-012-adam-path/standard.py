import torch


def adam_path(start, grads, rate, memory):
    parameter = torch.tensor(start, dtype=torch.float64)
    optimizer = torch.optim.Adam([parameter], lr=rate, betas=(memory, 0.9))
    history = []
    for gradient in grads:
        parameter.grad = torch.tensor(gradient, dtype=parameter.dtype)
        optimizer.step()
        history.append(parameter.item())
    return history
