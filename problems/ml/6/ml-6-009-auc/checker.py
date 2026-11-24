from dojo_compare import allclose


def check_function(args, expected, fn):
    actual = fn(np.asarray(args[0]), np.asarray(args[1]))
    difference = allclose(expected, actual)
    assert difference is None, difference
    return True
