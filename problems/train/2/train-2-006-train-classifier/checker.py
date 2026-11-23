import torch
from dojo_train import simulate_train, assert_loss_decreased, assert_trajectory


def check_function(args, expected, fn):
    seed = args[0]
    seen = {}

    def make_model():
        model = torch.nn.Linear(1, 2)

        def observe(module, inputs, output):
            seen["input"] = inputs[0].detach().clone()
            seen["scores"] = output.detach().clone()

        model.register_forward_hook(observe)
        return model

    def batches():
        x = torch.tensor([[-1.5], [-0.5], [0.5], [1.5]])
        y = (x[:, 0] > 0).long()
        valid_x = x * 0.8
        seen["valid_x"] = valid_x
        seen["valid_y"] = y
        return (x, y), (valid_x, seen["valid_y"])

    def objective(scores, labels):
        raw = seen["scores"]
        assert scores.shape == raw.shape and torch.allclose(scores, raw), "交叉熵需要模型的原始分数，请检查是否提前做了 softmax"
        assert labels.dtype == torch.long and labels.shape == (len(scores),), "每行需要一个 long 类别下标，形状应为 (批大小,)"
        wanted = (seen["input"][:, 0] > 0).long()
        if torch.equal(seen["input"], seen["valid_x"]):
            wanted = seen["valid_y"]
        assert torch.equal(labels, wanted), "特征和标签没有使用同一组行号"
        return torch.nn.functional.cross_entropy(scores, labels)

    def reference(model, data, optimizer, steps):
        x, y = data.train
        for _ in range(steps):
            loss = data.loss(model(x), y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        seen["final"] = [p.detach().clone() for p in model.parameters()]

    def observed(model, data, optimizer, steps):
        fn(model, data, optimizer, steps)

        seen["actual"] = [p.detach().clone() for p in model.parameters()]

    options = dict(make_model=make_model, make_data=batches, loss_fn=objective,
                   make_optimizer=lambda params: torch.optim.SGD(params, lr=0.25), steps=24, seed=seed)
    reference_losses = simulate_train(reference, **options)
    losses = simulate_train(observed, require_eval=False, **options)
    assert_trajectory(losses, reference_losses, rtol=1e-5, atol=1e-6)
    for actual, wanted in zip(seen["actual"], seen["final"]):
        assert torch.allclose(actual, wanted, atol=1e-6, rtol=1e-5), "最后一次更新后的参数偏离参考结果，请核对更新顺序和步长"
    assert_loss_decreased(losses, window=4, ratio=0.75)
    return True
