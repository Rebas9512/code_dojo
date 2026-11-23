import torch
from torch.utils.data import DataLoader, Dataset


def check_function(args, expected, fn):
    rows, order, held, width = args
    loader = fn(*args)
    assert isinstance(loader, DataLoader) and isinstance(loader.dataset, Dataset), "请返回使用 Dataset 的 DataLoader"
    chosen = [rows[i] for i in order[held:]]
    assert len(loader.dataset) == len(chosen), "请从数据集中排除留出的行"
    for i, row in enumerate(chosen):
        assert list(loader.dataset[i]) == row, f"训练数据集第 {i} 条与行号不符"
    batches = list(loader)
    count = (len(chosen) + width - 1) // width
    assert len(batches) == count, "请保留短末批"
    for i, actual in enumerate(batches):
        batch = chosen[i*width:(i+1)*width]
        longest = max(map(len, batch))
        wanted = [row + [-1] * (longest - len(row)) for row in batch]
        assert isinstance(actual, torch.Tensor) and actual.dtype == torch.long, "每批需要一个 long 张量"
        assert actual.tolist() == wanted, "以本批最长句为准，在右侧补 −1"
    return True
