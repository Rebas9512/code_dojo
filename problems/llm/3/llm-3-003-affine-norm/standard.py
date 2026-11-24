import torch


def standardize(x, eps):
    x = torch.tensor(x, dtype=torch.float32)
    delta = x - torch.mean(x, dim=-1, keepdim=True)
    variance = torch.mean(delta * delta, dim=-1, keepdim=True)
    return delta / torch.sqrt(variance + eps)


def affine_norm(x, gamma, beta, eps):
    return standardize(x, eps) * torch.tensor(gamma) + torch.tensor(beta)
