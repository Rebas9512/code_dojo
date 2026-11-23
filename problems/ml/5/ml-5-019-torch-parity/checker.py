import numpy as np
from dojo_compare import allclose


def check_function(args, expected, network):
    X, W1, b1, W2, b2, G = [np.asarray(a, dtype=float) for a in args]
    h = np.tanh(X @ W1 + b1)
    hidden_grad = (G @ W2.T) * (1 - h*h)
    reference = [h @ W2 + b2, hidden_grad @ W1.T, X.T @ hidden_grad,
                 hidden_grad.sum(axis=0), h.T @ G, G.sum(axis=0)]
    result = network(*args)
    assert len(result) == len(reference), "应返回输出和五份梯度"
    for name, want, got in zip(("Y", "dX", "dW1", "db1", "dW2", "db2"), reference, result):
        reason = allclose(want, got, rtol=1e-7, atol=1e-9)
        assert reason is None, f"{name} 对拍失败。{reason}"
    return True
