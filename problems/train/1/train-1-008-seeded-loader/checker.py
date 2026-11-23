import torch
from torch.utils.data import DataLoader

def check_function(args, expected, fn):
    values, width, seed = args
    loader = fn(*args)
    assert isinstance(loader, DataLoader), "请返回可继续遍历的 DataLoader"
    for epoch in range(2):
        if epoch == 0:
            reference = DataLoader(values, batch_size=width, shuffle=True,
                                   generator=torch.Generator().manual_seed(seed))
        observed = [b.tolist() for b in loader]
        wanted = [b.tolist() for b in reference]
        assert observed == wanted, f"第 {epoch + 1} 轮的批次与指定种子不符"
    return True
