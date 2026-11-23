import torch


def momentum_path(start, grads, rate, memory):
    p = torch.tensor(float(start), dtype=torch.float64, requires_grad=True)
    opt = torch.optim.SGD([p], lr=rate, momentum=memory)
    history = []
    for g in grads:
        p.grad = torch.tensor(g, dtype=p.dtype)
        opt.step()
        history.append(p.item())
    return history
