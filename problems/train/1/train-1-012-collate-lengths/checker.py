import torch
from torch.utils.data import DataLoader

def check_function(args, expected, fn):
    rows = args[0]
    loader = DataLoader(rows, batch_size=len(rows), collate_fn=fn)
    padded, lengths = next(iter(loader))
    assert list(lengths) == list(map(len, rows)), "请保留补齐前的长度，真实零也占位置"
    wanted = [row + [0] * (max(lengths) - len(row)) for row in rows]
    assert isinstance(padded, torch.Tensor) and padded.dtype == torch.long, "请返回 long 整数张量"
    assert padded.tolist() == wanted, "按样本排成行并在右侧补零"
    return True
