import torch
from torch import nn
from dojo_compare import allclose


def check_function(args, expected, fn):
    initial, first, second = [torch.tensor(v, dtype=torch.float32) for v in args]
    meter = fn(args[0])
    assert isinstance(meter, nn.Module), "请返回自定义模块。"
    gain = dict(meter.named_parameters()).get("gain")
    assert gain is not None and gain.requires_grad, "需要可训练的 gain 参数。"
    reason = allclose(initial, gain) or allclose(initial * first, meter(first))
    assert reason is None, reason
    meter.record(first)
    reason = allclose(first, gain.grad)
    assert reason is None, reason
    meter.record(second)
    reason = allclose(expected, gain.grad)
    assert reason is None, "第二笔应加在第一笔之后。" + str(reason)
    return True
