import torch
from torch import nn
from dojo_compare import allclose


def check_function(args, expected, fn):
    w, b = [torch.tensor(a, dtype=torch.float32) for a in args]
    model = fn(*args)
    assert isinstance(model, nn.Linear), "需要一个 Linear 层。"
    assert model.bias is not None and model.weight.requires_grad and model.bias.requires_grad, "权重和偏置都要可学习。"
    reason = allclose(w, model.weight) or allclose(b, model.bias)
    assert reason is None, reason
    x = torch.arange(2 * w.shape[1], dtype=w.dtype).reshape(2, -1)
    reason = allclose(x @ w.T + b, model(x))
    assert reason is None, reason
    return True
