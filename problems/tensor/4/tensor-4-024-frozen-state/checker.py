import torch
from torch import nn
from dojo_compare import allclose


def check_function(args, expected, fn):
    weights, bias = [torch.tensor(a, dtype=torch.float32) for a in args]
    torch.manual_seed(0)
    layer = nn.Linear(weights.shape[1], weights.shape[0])
    with torch.no_grad():
        layer.weight.copy_(weights)
        layer.bias.copy_(bias)
    snapshot = fn(layer)
    assert isinstance(snapshot, dict) and snapshot.keys() == expected.keys(), "请保存每个状态名。"
    with torch.no_grad():
        layer.weight.add_(11)
        layer.bias.add_(13)
    for key in expected:
        assert isinstance(snapshot[key], torch.Tensor), "每项状态都应是张量。"
        reason = allclose(expected[key], snapshot[key])
        assert reason is None, "更新后快照应保留旧值。" + str(reason)
    return True
