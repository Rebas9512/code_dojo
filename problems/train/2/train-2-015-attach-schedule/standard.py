import torch


def make_schedule(optimizer, period, factor):
    return torch.optim.lr_scheduler.StepLR(optimizer, step_size=period, gamma=factor)
