import torch
from dojo_grad import check_grad


def check_function(args, expected, fn):
    x = torch.tensor(args[0], dtype=torch.float64)
    return check_grad(fn, lambda t: ((t - 1) ** 2).sum(), [x])
