import torch

def check_function(args, expected, fn):
    grads, bound = args
    torch.manual_seed(0)
    model = torch.nn.Linear(len(grads), 1, bias=False)
    opt = torch.optim.SGD(model.parameters(), lr=0.25)
    x = torch.tensor(grads)
    old = model.weight.detach().clone()
    model.weight.grad = torch.ones_like(model.weight)
    fn(model, model(x).sum(), opt, bound)
    target = old - 0.25 * x * min(1., bound / (x.norm().item() + 1e-6))
    assert torch.allclose(model.weight, target, atol=1e-6), "请清掉旧梯度，并在 step 前按总范数裁剪"
    return True
