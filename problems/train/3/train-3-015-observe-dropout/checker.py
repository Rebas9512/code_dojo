import torch

def check_function(args, expected, fn):
    seed = args[0]
    layer = torch.nn.Dropout(0.5).eval()
    x = torch.arange(1, 13, dtype=torch.float32, requires_grad=True)
    calls = []
    layer.register_forward_pre_hook(lambda m,a: calls.append((m.training, torch.is_grad_enabled())))
    train, valid = fn(layer, x, seed)
    assert len(calls) == 2 and calls[0][0] and calls[1] == (False, False), "按训练、验证顺序各调用一次，验证时关闭梯度"
    torch.manual_seed(seed)
    assert torch.equal(train, torch.nn.functional.dropout(x,0.5,True)), "训练掩码与种子不符"
    assert torch.equal(valid, x) and not layer.training, "验证时保留所有输入"
    return True
