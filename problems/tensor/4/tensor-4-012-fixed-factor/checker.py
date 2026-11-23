import torch
from dojo_compare import allclose


def check_function(args, expected, fn):
    x = torch.tensor(args[0], dtype=torch.float64, requires_grad=True)
    original = x.detach().clone()
    y = fn(x)
    reason = allclose(expected, y)
    assert reason is None, reason
    assert isinstance(y, torch.Tensor) and y.requires_grad, "乘积要保留左因子的路径。"
    weights = torch.arange(1, x.numel() + 1, dtype=x.dtype)
    (y * weights).sum().backward()
    reason = allclose(original * weights, x.grad)
    assert reason is None, "请只让左因子贡献梯度。" + str(reason)
    return True
