import torch

def check_function(args, expected, fn):
    p, training = args
    layer = fn(*args)
    assert isinstance(layer, torch.nn.Dropout) and layer.p == p, "检查丢弃概率"
    assert layer.training == training, "training 为假时应进入验证模式"
    x = torch.arange(8, dtype=torch.float32)
    torch.manual_seed(0)
    out = layer(x)
    torch.manual_seed(0)
    assert torch.equal(out, torch.nn.functional.dropout(x, p, training)), "检查前向的丢弃行为"
    return True
