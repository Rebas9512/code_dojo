import dataclasses
import random

import numpy as np
import torch


def check_function(args, expected, cls):
    overrides, = args[0]
    defaults = dict(seed=42, epochs=40, batch_size=64, hidden_size=96, lr=0.006,
                    weight_decay=0.01, step_size=12, gamma=0.5, max_norm=1.0, patience=10)
    assert dataclasses.is_dataclass(cls), "请用 @dataclass 声明配置"
    config = cls(**overrides)
    for name, value in (defaults | overrides).items():
        assert getattr(config, name) == value, f"请检查配置字段 {name} 的值"
    seed = config.seed
    python_rng = random.Random(seed)
    numpy_rng = np.random.RandomState(seed)
    torch_rng = torch.Generator().manual_seed(seed)
    draws = ([python_rng.random() for _ in range(3)], numpy_rng.rand(3), torch.rand(3, generator=torch_rng))
    for _ in range(2):
        config.set_seed()
        assert [random.random() for _ in range(3)] == draws[0], "Python 的序列没有回到指定起点"
        assert np.array_equal(np.random.rand(3), draws[1]), "NumPy 的序列没有回到指定起点"
        assert torch.equal(torch.rand(3), draws[2]), "PyTorch 的序列没有回到指定起点"
    return True
