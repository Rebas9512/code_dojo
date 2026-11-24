def check_function(args, expected, fn):
    prompt, steps, k, temperature, seed = args
    torch.manual_seed(171)
    model = GPT(7, 8, 12, 3, 2).eval()
    rng = torch.Generator().manual_seed(seed)
    original = list(prompt)
    want = list(prompt)
    with torch.no_grad():
        for _ in range(steps):
            logits, _, _ = model(torch.tensor([want]))
            want.append(sample_token(logits[0, -1], temperature, k, rng))

    for use_cache in (False, True):
        calls = []
        def observe(module, inputs):
            calls.append((inputs[0].tolist(), torch.is_grad_enabled()))
        hook = model.register_forward_pre_hook(observe)
        got = fn(model, prompt, steps, temperature, k, seed, use_cache)
        hook.remove()
        assert got == want, "有无缓存的完整编号串都应等于逐步重算的结果"
        feeds = [want[:len(prompt) + i] for i in range(steps)]
        if use_cache:
            feeds[1:] = [[row[-1]] for row in feeds[1:]]
        assert calls == [([row], False) for row in feeds], "检查模型实际收到的输入及梯度开关"
    return prompt == original
