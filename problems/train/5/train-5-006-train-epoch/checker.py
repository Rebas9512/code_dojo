import math

import torch
from dojo_train import simulate_train, assert_trajectory


def check_function(args, expected, fn):
    n, width, max_norm, seed = args
    snapshots = []

    def make_data():
        x = torch.randn(n, 3) * 3
        y = torch.arange(n) % 2
        return (x, y), (x.clone(), y.clone())

    def run(epoch_fn):
        def observed(model, data, optimizer, steps):
            model.eval()
            x, y = data.train
            batches = list(zip(x.split(width), y.split(width)))
            mean_loss = epoch_fn(model, batches, optimizer, data.loss, max_norm)
            assert isinstance(mean_loss, float), "请返回脱离计算图的 Python 浮点数"
            snapshots.append(([p.detach().clone() for p in model.parameters()], mean_loss))
        return simulate_train(observed, make_model=lambda: torch.nn.Linear(3, 2),
                              make_data=make_data, make_optimizer=lambda p: torch.optim.SGD(p, lr=0.2),
                              loss_fn=torch.nn.functional.cross_entropy, steps=(n + width - 1) // width, seed=seed)

    def reference(model, batches, optimizer, loss_fn, limit):
        model.train()
        total = 0.0
        for features, labels in batches:
            optimizer.zero_grad()
            loss = loss_fn(model(features), labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), limit)
            optimizer.step()
            total += loss.item() * len(labels)
        return total / n

    wanted = run(reference)
    actual = run(fn)
    assert_trajectory(actual, wanted, atol=1e-6)
    (weights, mean), (got, value) = snapshots
    assert all(torch.allclose(a, b, atol=1e-6) for a, b in zip(weights, got)), "最后的权重不同，请在每次更新前按总范数裁剪"
    assert math.isclose(mean, value, rel_tol=1e-6, abs_tol=1e-7), "每批平均损失要按实际批大小加权"
    return True
