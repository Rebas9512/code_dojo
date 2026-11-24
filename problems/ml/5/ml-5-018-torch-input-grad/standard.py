import torch


def input_grad(X, W1, b1, W2, b2, G):
    x = torch.tensor(X, dtype=torch.float64, requires_grad=True)
    W1, b1, W2, b2, upstream = [
        torch.tensor(value, dtype=torch.float64) for value in (W1, b1, W2, b2, G)
    ]
    hidden = torch.tanh(x @ W1 + b1)
    output = hidden @ W2 + b2
    torch.sum(output * upstream).backward()
    return x.grad
