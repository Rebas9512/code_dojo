import torch
from torch import nn
from dojo_compare import allclose


def check_function(args, expected, fn):
    weights, bias = [torch.tensor(a, dtype=torch.float32) for a in args]
    torch.manual_seed(0)
    layer = nn.Linear(weights.shape[1], weights.shape[0])
    saved = {"weight": weights, "bias": bias}
    fn(layer, saved)
    reason = allclose(weights, layer.weight) or allclose(bias, layer.bias)
    assert reason is None, reason
    y = layer(torch.ones(weights.shape[1]))
    reason = allclose(expected, y)
    assert reason is None, reason
    return True
