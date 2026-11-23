from torch.utils.data import Dataset

def check_function(args, expected, fn):
    values, labels = args
    ds = fn(values, labels)
    assert isinstance(ds, Dataset), "请返回 Dataset 实例"
    assert len(ds) == len(values), "长度要数样本"
    for i in reversed(range(len(values))):
        assert tuple(ds[i]) == (values[i], labels[i]), f"下标 {i} 的值和标签没有配对"
    return True
