def make_optimizer(model, config):
    from torch.optim import AdamW
    from torch.optim.lr_scheduler import StepLR

    optimizer = AdamW(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)
    scheduler = StepLR(optimizer, step_size=config.step_size, gamma=config.gamma)
    return optimizer, scheduler
