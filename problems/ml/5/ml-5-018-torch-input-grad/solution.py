import torch


def input_grad(X, W1, b1, W2, b2, G):
    x = torch.tensor(X, dtype=torch.float64, requires_grad=True)
    w, b, v, c, g = [torch.tensor(a, dtype=torch.float64) for a in (W1, b1, W2, b2, G)]
    y = torch.tanh(x @ w + b) @ v + c
    torch.sum(y * g).backward()
    return x.grad
