import torch

def check_function(args, expected, fn):
    grads, bound = args
    ps = [torch.nn.Parameter(torch.tensor(0.)) for g in grads]
    for p,g in zip(ps, grads):
        p.grad = torch.tensor(g)
    fn(ps, bound)
    v = torch.tensor(grads)
    expected = v * min(1., bound / (v.norm().item() + 1e-6))
    assert torch.allclose(torch.stack([p.grad for p in ps]), expected, atol=1e-6), "要用所有参数的总长度确定同一缩放比例"
    return True
