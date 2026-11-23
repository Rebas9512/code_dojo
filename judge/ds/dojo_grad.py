"""用中心差分核对标量函数对一个或多个输入的梯度。"""

import math

import numpy as np

from dojo_compare import allclose


def _copy(x):
    if hasattr(x, "detach"):
        return x.detach().double().clone()
    return np.array(x, dtype=np.float64, copy=True)


def _scalar(value):
    if np.shape(value) != ():
        raise ValueError("数值梯度要求 f 返回标量，向量输出请先与上游梯度做内积")
    return float(value)


def numeric_grad(f, x, eps=1e-5):
    if not math.isfinite(eps) or eps <= 0:
        raise ValueError("eps 必须是有限正数")
    point = _copy(x)
    grad = _copy(x)
    for index in np.ndindex(tuple(point.shape)):
        original = float(point[index])
        point[index] = original + eps
        high = _scalar(f(point))
        point[index] = original - eps
        low = _scalar(f(point))
        point[index] = original
        grad[index] = (high - low) / (2 * eps)
    return grad


def check_grad(user_backward, f, inputs, *, eps=1e-5, rtol=1e-4, atol=1e-6):
    """inputs 是位置参数序列。一个输入直接返回梯度，多个输入按顺序返回各梯度。"""
    points = [_copy(x) for x in inputs]
    if not points:
        raise ValueError("梯度检查至少需要一个输入")
    actual = user_backward(*[_copy(x) for x in points])
    grads = [actual] if len(points) == 1 else actual
    if not isinstance(grads, (tuple, list)) or len(grads) != len(points):
        raise AssertionError(f"应按输入顺序返回 {len(points)} 个梯度")
    for i, point in enumerate(points):
        def partial(x):
            return f(*points[:i], x, *points[i + 1:])

        expected = numeric_grad(partial, point, eps)
        reason = allclose(expected, grads[i], rtol=rtol, atol=atol)
        if reason:
            raise AssertionError(f"第 {i + 1} 个输入的梯度不符。{reason}")
    return True
