import torch
from torch.utils.data import DataLoader

def check_function(args, expected, fn):
    xs, ys, width, seed = args
    ids = DataLoader(range(len(xs)), batch_size=width, shuffle=True,
                     generator=torch.Generator().manual_seed(seed))
    wanted = [[[xs[i] for i in batch], [ys[i] for i in batch]] for batch in ids]
    assert fn(*args) == wanted, "请用同一组洗牌行号取值和标签，并保留末批"
    return True
