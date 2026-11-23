import sys

import torch
from dojo_compare import allclose


def check_function(args, expected, fn):
    inputs = [torch.tensor(value) for value in args]
    a, p = inputs
    reference = a @ p
    # 记录实际执行的 einsum，别名和 from 导入也会经过同一函数。
    calls = []

    def observe(frame, event, arg):
        if event == "call" and frame.f_code is torch.einsum.__code__:
            calls.append(True)

    previous = sys.getprofile()
    try:
        sys.setprofile(observe)
        actual = fn(*inputs)
    finally:
        sys.setprofile(previous)
    assert calls, "请用 torch.einsum 写出轴的配对。"
    reason = allclose(reference, actual)
    assert reason is None, reason
    return True
