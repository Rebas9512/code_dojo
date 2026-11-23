import torch
from dojo_train import simulate_train, assert_loss_decreased, assert_overfit, assert_trajectory

def batches():
    x = torch.tensor([[-1.0], [1.0]])
    return (x, 2 * x), (x / 2, x)

def reference(model, data, optimizer, steps):
    x, y = data.train
    for _ in range(steps):
        optimizer.zero_grad()
        data.loss(model(x), y).backward()
        optimizer.step()

def check_function(args, expected, train):
    options = dict(make_model=lambda: torch.nn.Linear(1, 1), make_data=batches,
                   make_optimizer=lambda params: torch.optim.SGD(params, lr=0.25),
                   loss_fn=torch.nn.functional.mse_loss, steps=24, seed=args[0])
    losses = simulate_train(train, require_eval=True, **options)
    assert_loss_decreased(losses)
    assert_overfit(losses)
    assert_trajectory(losses, simulate_train(reference, **options))
    return True
