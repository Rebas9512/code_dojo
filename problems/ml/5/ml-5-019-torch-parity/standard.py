import torch


def network(X, W1, b1, W2, b2, G):
    X, W1, b1, W2, b2 = [
        torch.tensor(value, dtype=torch.float64, requires_grad=True)
        for value in (X, W1, b1, W2, b2)
    ]
    hidden = torch.tanh(X @ W1 + b1)
    output = hidden @ W2 + b2
    upstream = torch.tensor(G, dtype=torch.float64)
    torch.sum(output * upstream).backward()
    return output.detach(), X.grad, W1.grad, b1.grad, W2.grad, b2.grad
