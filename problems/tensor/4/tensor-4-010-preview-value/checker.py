import torch
from dojo_compare import allclose


def check_function(args, expected, fn):
    x = torch.tensor(args[0], dtype=torch.float32, requires_grad=True)
    y = fn(x)
    assert isinstance(y, torch.Tensor) and not y.requires_grad, "预览应是无需梯度的张量。"
    assert x.requires_grad and torch.equal(x, torch.tensor(args[0], dtype=x.dtype)), "请保留原输入。"
    reason = allclose(expected, y)
    assert reason is None, reason
    return True
