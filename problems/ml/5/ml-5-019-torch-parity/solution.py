import torch


def network(X, W1, b1, W2, b2, G):
    params = [torch.tensor(a, dtype=torch.float64, requires_grad=True) for a in (X, W1, b1, W2, b2)]
    X, W1, b1, W2, b2 = params
    Y = torch.tanh(X @ W1 + b1) @ W2 + b2
    upstream = torch.tensor(G, dtype=torch.float64)
    torch.sum(Y * upstream).backward()
    return (Y.detach(), X.grad, W1.grad, b1.grad, W2.grad, b2.grad)
