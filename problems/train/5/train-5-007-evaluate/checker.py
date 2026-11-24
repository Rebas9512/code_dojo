import math

import torch


def check_function(args, expected, fn):
    matches, width = args
    labels = torch.arange(len(matches)) % 3
    predicted = (labels + ~torch.tensor(matches)) % 3
    features = torch.nn.functional.one_hot((predicted + 1) % 3, 3).float()
    model = torch.nn.Linear(3, 3, bias=False)
    weights = torch.eye(3).roll(1, dims=1)
    with torch.no_grad():
        model.weight.copy_(weights)
    observed = []

    def observe(layer, inputs):
        observed.append(len(inputs[0]))
        assert not layer.training, "验证前请切换到 eval 模式"
        assert not torch.is_grad_enabled(), "验证前向需要关闭梯度记录"

    model.register_forward_pre_hook(observe)
    batches = list(zip(features.split(width), labels.split(width)))
    with torch.enable_grad():
        value = fn(model, batches)
        assert torch.is_grad_enabled(), "离开验证后需要恢复梯度开关，下一轮还要训练"
    assert sum(observed) == len(labels), "每张验证图应交给模型测量一次"
    assert isinstance(value, float) and math.isclose(value, expected, abs_tol=1e-7), "分母应是所有验证样本的实际数量"
    assert torch.equal(model.weight, weights) and model.weight.grad is None, "验证只测量，不更新模型"
    return True
