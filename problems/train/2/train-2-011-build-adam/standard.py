import torch


def make_adam(params, rate, first, second):
    return torch.optim.Adam(params, lr=rate, betas=(first, second))
