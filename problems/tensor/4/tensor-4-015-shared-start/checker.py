import torch
from torch import nn
from dojo_compare import allclose


def check_function(args, expected, fn):
    p = fn(*args)
    assert isinstance(p, nn.Parameter) and p.is_leaf and p.requires_grad, "需要可学习的叶子 Parameter。"
    reason = allclose(expected, p)
    assert reason is None, reason
    return True
