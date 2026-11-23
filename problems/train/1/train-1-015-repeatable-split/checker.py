import torch

def check_function(args, expected, fn):
    n, count, seed = args
    ids = torch.randperm(n, generator=torch.Generator().manual_seed(seed)).tolist()
    train, valid = fn(*args)
    assert not set(train).intersection(valid), "训练和验证出现了同一行号"
    assert [train, valid] == [ids[count:], ids[:count]], "请从同一个指定种子的排列切出两段"
    return True
