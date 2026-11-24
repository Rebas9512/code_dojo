def check_function(args, expected, fn):
    shapes, lr, decay = args
    model = nn.ParameterList([nn.Parameter(torch.ones(shape)) for shape in shapes])
    opt = fn(model, lr, decay)
    assert isinstance(opt, torch.optim.AdamW), "需要 AdamW 优化器"
    seen = []
    for group in opt.param_groups:
        assert group["lr"] == lr, "每组都应使用传入的初始学习率"
        for p in group["params"]:
            assert group["weight_decay"] == (decay if p.ndim == 2 else 0)
            seen.append(id(p))
    return sorted(seen) == sorted(map(id, model.parameters()))
