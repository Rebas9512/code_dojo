import torch
from torch import nn
from dojo_compare import allclose


def check_function(args, expected, fn):
    model = fn(*args)
    assert isinstance(model, nn.Module), "请返回 nn.Module 实例。"
    values = [torch.tensor(a, dtype=torch.float32) for a in args]
    params = dict(model.named_parameters())
    assert set(params) == set(['gain', 'offset']), "请按题意登记参数。"
    for name, initial in zip(['gain', 'offset'], values):
        reason = allclose(initial, params[name])
        assert reason is None and params[name].requires_grad, "请检查参数初值和求导开关。"
    x = torch.arange(2 * values[0].numel(), dtype=torch.float32).reshape(2, -1)
    y = model(x)
    reference = x * values[0] + values[1]
    reason = allclose(reference, y)
    assert reason is None, reason
    y.sum().backward()
    for name in ['gain', 'offset']:
        assert params[name].grad is not None, "前向需保留到参数的梯度路径。"
    return True
