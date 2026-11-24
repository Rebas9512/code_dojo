import torch


def make_sgd(params, rate, momentum):
    return torch.optim.SGD(params, lr=rate, momentum=momentum)
