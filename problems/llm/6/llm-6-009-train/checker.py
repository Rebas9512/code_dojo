def check_function(args, expected, fn):
    steps, every, batches, seed, clip = args
    cfg = SimpleNamespace(steps=steps, eval_every=every, eval_batches=batches, seed=seed,
                          warmup=1, peak=0.25, floor=0.05, clip=clip, batch_size=2, context=3)
    data = TextWindows(list(range(100)))
    class Probe(nn.Module):
        def __init__(self):
            super().__init__()
            self.weight = nn.Parameter(torch.tensor(2.0))
            self.calls = []

        def forward(self, x, y):
            self.calls.append((self.training, torch.is_grad_enabled(), x.tolist(), y.tolist()))
            loss = (self.weight - y.float().mean() / 12).square()
            return None, loss, None

    model = Probe()
    opt = torch.optim.SGD(model.parameters(), lr=0.9)
    history = fn(model, data, opt, cfg)
    train_rng = torch.Generator().manual_seed(seed)
    expected_calls = []
    expected_history = []
    weight = 2.0
    for step in range(steps + 1):
        if step:
            x, y = data.get_batch("train", 2, 3, train_rng)
            expected_calls.append((True, True, x.tolist(), y.tolist()))
            grad = 2 * (weight - y.float().mean().item() / 12)
            ratio = min(1.0, clip / (abs(grad) + 1e-6))
            weight -= learning_rate(step, steps, 1, 0.25, 0.05) * grad * ratio
        if step % every == 0 or step == steps:
            valid_rng = torch.Generator().manual_seed(seed + 1)
            losses = []
            for _ in range(batches):
                x, y = data.get_batch("valid", 2, 3, valid_rng)
                expected_calls.append((False, False, x.tolist(), y.tolist()))
                losses.append((weight - y.float().mean().item() / 12) ** 2)
            expected_history.append((step, sum(losses) / batches))
    assert model.calls == expected_calls, "检查训练与验证的批次、模式、梯度开关和次数"
    assert math.isclose(model.weight.item(), weight, abs_tol=1e-5), "检查清梯度、裁剪和学习率"
    torch.testing.assert_close(torch.tensor(history), torch.tensor(expected_history))
    return not model.training
