import torch
from dojo_train import simulate_train, assert_trajectory, assert_loss_decreased


def check_function(args, expected, trace):
    start, target, rate, steps = args

    def model():
        layer = torch.nn.Linear(1, 1, bias=False, dtype=torch.float64)
        with torch.no_grad():
            layer.weight.fill_(start)
        return layer

    def batches():
        pair = (torch.ones((1, 1), dtype=torch.float64), torch.tensor([[target]], dtype=torch.float64))
        return pair, pair

    def train(layer, data, optimizer, count):
        x, y = data.train
        for _ in range(count):
            optimizer.zero_grad()
            data.loss(layer(x), y).backward()
            optimizer.step()

    reference = simulate_train(train, model, batches, lambda p: torch.optim.SGD(p, lr=rate),
                               torch.nn.functional.mse_loss, steps=steps, seed=0)
    losses = list(trace(*args))
    assert_trajectory(losses, reference)
    if 0 < rate < 1 and start != target:
        assert_loss_decreased(losses, window=1, ratio=1)
    return True
