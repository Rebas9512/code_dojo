import torch
from torch import nn


def check_function(args, expected, fn):
    hidden, batch = args
    torch.manual_seed(hidden)
    model = fn(hidden)
    layers = [layer for layer in model.modules() if isinstance(layer, nn.Linear)]
    assert len(layers) == 2, "小 MLP 需要两层带偏置的线性变换"
    first, last = layers
    assert (first.in_features, first.out_features, last.in_features, last.out_features) == (64, hidden, hidden, 10), "检查输入、隐藏和输出宽度"
    assert first.bias is not None and last.bias is not None, "两层均保留偏置"
    x = torch.randn(batch, 64)
    scores = model(x)
    reference = last(torch.relu(first(x)))
    assert scores.shape == (batch, 10) and torch.allclose(scores, reference), "在两层之间使用 ReLU，最后返回原始分数"
    grads = torch.autograd.grad(scores.sum(), list(model.parameters()))
    assert len(grads) == 4, "两层的权重与偏置都应参与训练"
    return True
