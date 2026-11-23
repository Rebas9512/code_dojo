import torch
import math

def check_function(args, expected, fn):
    period, factor = args
    params = [torch.nn.Parameter(torch.tensor(0.)) for _ in range(2)]
    opt = torch.optim.SGD([{"params":[params[i]], "lr":v} for i,v in enumerate([0.8,0.2])])
    sched = fn(opt, period, factor)
    for epoch in range(2 * period + 1):
        for group, start in zip(opt.param_groups, [0.8, 0.2]):
            assert math.isclose(group["lr"], start * factor ** (epoch // period)), f"第 {epoch+1} 轮的步长不符"
        opt.step()
        sched.step()
    return True
