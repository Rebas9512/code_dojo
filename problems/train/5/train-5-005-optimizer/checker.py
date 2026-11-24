import math

import torch


def check_function(args, expected, fn):
    lr, decay, step_size, gamma = args
    config = Config(lr=lr, weight_decay=decay, step_size=step_size, gamma=gamma)
    model = torch.nn.Linear(3, 2)
    optimizer, scheduler = fn(model, config)
    assert isinstance(optimizer, torch.optim.AdamW), "使用 AdamW 的解耦权重衰减"
    assert isinstance(scheduler, torch.optim.lr_scheduler.StepLR) and scheduler.optimizer is optimizer, "StepLR 应管理同一个优化器"
    params = [p for group in optimizer.param_groups for p in group["params"]]
    assert sorted(map(id, params)) == sorted(map(id, model.parameters())), "请将模型的所有参数交给优化器"
    for epoch in range(2 * step_size + 1):
        for group in optimizer.param_groups:
            assert group["weight_decay"] == decay, "权重衰减应取自配置"
            assert math.isclose(group["lr"], lr * gamma ** (epoch // step_size)), "学习率与轮末衰减日历不符"
        optimizer.step()
        scheduler.step()
    return True
