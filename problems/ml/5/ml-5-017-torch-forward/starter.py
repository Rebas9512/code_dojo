import torch


def forward(X, W1, b1, W2, b2):
    X, W1, b1, W2, b2 = [torch.tensor(a, dtype=torch.float64) for a in (X, W1, b1, W2, b2)]
    h = ...  # 补全这里
    return h @ W2 + b2
