import torch

def check_function(args, expected, fn):
    torch.manual_seed(args[0])
    x = torch.randn(3, 2, requires_grad=True)
    model = torch.nn.Linear(2, 1)
    calls = []
    model.register_forward_pre_hook(lambda m, a: calls.append((m.training, torch.is_grad_enabled())))
    actual = fn(model, x)
    assert calls and all(c == (False,False) for c in calls), "请先切到 eval，并在 no_grad 中完成模型前向"
    assert not model.training and not actual.requires_grad, "验证结束时保留评估模式，输出应无梯度记录"
    with torch.no_grad():
        assert torch.allclose(actual, model(x)), "返回验证批上的模型输出"
    return True
