import torch


def regularized(params, rate, decay):
    return torch.optim.SGD(params, lr=rate, weight_decay=decay)
