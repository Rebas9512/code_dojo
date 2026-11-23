import numpy as np
from dojo_grad import check_grad
from dojo_compare import allclose


def expression(a, b, op, kind):
    shared = a * b + a
    if kind == 0:
        return shared + shared
    if kind == 1:
        return op(shared) * shared
    if kind == 2:
        return (a + b) * (a + a * b)
    if kind == 3:
        return a * a + b * b
    return op(a + a) + op(b * a)


def check_function(args, expected, make_value):
    x, y, kind = args

    def objective(a, b):
        return expression(a, b, np.tanh, kind)

    def backward(a, b):
        first, second = make_value(float(a)), make_value(float(b))
        root = expression(first, second, lambda n: n.tanh(), kind)
        reason = allclose(float(objective(a, b)), root.data)
        assert reason is None, reason
        root.backward()
        grads = [first.grad, second.grad]
        root.backward()
        reason = allclose(grads, [first.grad, second.grad])
        assert reason is None, "重复反传前应清空可达节点的旧梯度"
        return grads

    return check_grad(backward, objective, [np.array(x), np.array(y)])
