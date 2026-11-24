import torch
from torch.utils.data import DataLoader, TensorDataset


def check_function(args, expected, fn):
    n, valid_size, batch_size, seed = args

    ids = torch.arange(n)
    dataset = TensorDataset(7 * ids + 13, (3 * ids + 2) % 10)

    def read(loader, size):
        batches = list(loader)
        lengths = [len(labels) for _, labels in batches]
        assert lengths == [min(batch_size, size - i) for i in range(0, size, batch_size)], "请保留末批并使用指定批大小"
        pixels = torch.cat([features for features, _ in batches])
        labels = torch.cat([labels for _, labels in batches])
        indices = (pixels - 13) // 7
        assert torch.equal(pixels, 7 * indices + 13), "加载器应从传入的数据集读取样本"
        assert torch.equal(labels, (3 * indices + 2) % 10), "洗牌时特征与标签必须使用同一行号"
        return indices.tolist()

    def two_epochs():
        train, valid = fn(dataset, valid_size, batch_size, seed)
        assert isinstance(train, DataLoader) and isinstance(valid, DataLoader), "请返回训练、验证两个 DataLoader"
        train_a = read(train, n - valid_size)
        valid_a = read(valid, valid_size)
        train_b = read(train, n - valid_size)
        assert read(valid, valid_size) == valid_a, "验证批次应按留出顺序重复读取"
        assert sorted(train_a + valid_a) == list(range(n)), "划分应互斥且覆盖所有行"
        assert sorted(train_a) == sorted(train_b), "下一轮仍应读取同一训练集"
        if len(train_a) >= 5:
            assert train_a != train_b, "两轮训练都按原序读取了，请开启洗牌"
        return train_a, valid_a, train_b

    first = two_epochs()
    order = torch.randperm(n, generator=torch.Generator().manual_seed(seed)).tolist()
    assert first[1] == order[:valid_size], "用指定种子生成排列，取前 valid_size 行留作验证"
    torch.manual_seed(seed + 1)
    assert two_epochs() == first, "划分与训练洗牌都需要独立于全局种子的生成器"
    return True
