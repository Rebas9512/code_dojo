import torch


def used_rates(rate, period, factor, epochs):
    p = torch.tensor(0., requires_grad=True)
    opt = torch.optim.SGD([p], lr=rate)
    scheduler = torch.optim.lr_scheduler.StepLR(opt, step_size=period, gamma=factor)
    rates = []
    for _ in range(epochs):
        rates.append(opt.param_groups[0]["lr"])
        opt.step()
        ____  # 在此补全
    return rates
