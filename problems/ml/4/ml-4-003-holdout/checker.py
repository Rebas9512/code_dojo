import numpy as np
from dojo_compare import allclose


def check_function(args, expected, holdout):
    X, y, count, seed = args
    order = np.random.default_rng(seed).permutation(len(y)).tolist()
    test, train = order[:count], order[count:]
    ref = [[rows[i] for i in ids] for rows, ids in ((X, train), (y, train), (X, test), (y, test))]
    result = holdout(*args)
    assert len(result) == 4, "需要四个部分"
    for name, want, got in zip(("训练特征", "训练标签", "测试特征", "测试标签"), ref, result):
        reason = allclose(want, got)
        assert reason is None, f"{name}有差异。{reason}"
    return True
