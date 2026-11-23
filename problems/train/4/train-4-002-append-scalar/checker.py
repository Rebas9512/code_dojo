import torch

def check_function(args, expected, fn):
    value = float(args[0]) / 4
    loss = torch.tensor(value, requires_grad=True) * 2
    log = [1.5]
    fn(log, loss)
    assert len(log) == 2 and log[0] == 1.5, "请保留原日志，追加一个条目"
    assert type(log[-1]) is float and log[-1] == loss.item(), "日志里只放本步的浮点数，用 item() 取值"
    return True
