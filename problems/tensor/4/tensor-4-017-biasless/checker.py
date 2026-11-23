import torch
from torch import nn


def check_function(args, expected, fn):
    model = fn(*args)
    assert isinstance(model, nn.Linear), "请返回 Linear 层。"
    assert model.bias is None, "本层只含权重。"
    assert model.weight.requires_grad and list(model.weight.shape) == expected, "权重形状或求导标记错误。"
    assert model(torch.ones(1, args[0])).shape == (1, args[1]), "输出特征数不符。"
    return True
