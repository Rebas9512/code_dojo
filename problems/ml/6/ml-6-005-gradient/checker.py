from dojo_compare import allclose


def check_function(args, expected, fn):
    design, labels, weights, l2 = args
    actual = fn(np.asarray(design), np.asarray(labels), np.asarray(weights), l2)
    assert isinstance(actual, np.ndarray), "请返回可以乘学习率的 NumPy 梯度数组"
    difference = allclose(expected, actual)
    assert difference is None, difference
    return True
