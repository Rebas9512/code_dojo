from dojo_compare import allclose


def check_function(args, expected, fn):
    design, labels, rate, l2, steps = args
    actual = fn(np.asarray(design), np.asarray(labels), rate, l2, steps)
    difference = allclose(expected, actual)
    assert difference is None, difference
    return True
