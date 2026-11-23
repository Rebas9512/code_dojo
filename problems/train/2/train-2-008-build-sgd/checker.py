import torch


def check_function(args, expected, fn):
    torch.manual_seed(0)
    settings = args
    p = torch.nn.Parameter(torch.tensor([1., -2.]))
    baseline = torch.nn.Parameter(p.detach().clone())
    opt = fn([p], *settings)
    assert isinstance(opt, torch.optim.SGD), "请构造约定类型的优化器"
    ref = torch.optim.SGD([baseline], lr=settings[0], momentum=settings[1])
    for i, numbers in enumerate(([2., -0.2], [0., 1.], [-1., 0.])):
        p.grad = torch.tensor(numbers)
        baseline.grad = p.grad.clone()
        opt.step()
        ref.step()
        assert torch.allclose(p, baseline, atol=1e-7), f"第 {i+1} 步参数偏离，请核对优化器设置及状态"
    return True
