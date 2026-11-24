def make_optimizer(model, lr, decay):
    matrices = []
    others = []
    for parameter in model.parameters():
        if parameter.ndim == 2:
            matrices.append(parameter)
        else:
            others.append(parameter)
    groups = [
        {"params": matrices, "weight_decay": decay},
        {"params": others, "weight_decay": 0.0},
    ]
    return torch.optim.AdamW(groups, lr=lr)
