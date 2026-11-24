from dojo_compare import allclose


def check_function(args, expected, fn):
    actual = fn(*(np.asarray(arg) for arg in args))
    assert isinstance(actual, np.ndarray), "后续需要按一组行号选取设计矩阵"
    difference = allclose(expected, actual)
    assert difference is None, difference
    return True
