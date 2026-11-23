from math import tanh
from dojo_compare import allclose


def check_function(args, expected, make_value):
    a, b = map(make_value, args)
    assert len(a.parents) == len(b.parents) == 0, "新建的叶子没有输入边"
    total, product, repeated = a + b, a * b, a * a
    last = product.tanh()
    t = tanh(args[0] * args[1])
    rows = [(a, args[0], []), (b, args[1], []),
            (total, sum(args), [(a, 1.), (b, 1.)]),
            (product, args[0] * args[1], [(a, args[1]), (b, args[0])]),
            (repeated, args[0] ** 2, [(a, args[0]), (a, args[0])]),
            (last, t, [(product, 1 - t*t)])]
    for node, want, edges in rows:
        reason = allclose([want, 0.0], [node.data, node.grad])
        assert reason is None, reason
        assert len(node.parents) == len(edges), "每个输入位置都应保留边"
        for (actual, slope), (parent, derivative) in zip(node.parents, edges):
            assert actual is parent, "边应指向原来的输入节点"
            reason = allclose(float(derivative), float(slope))
            assert reason is None, reason
    return True
