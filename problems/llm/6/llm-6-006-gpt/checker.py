def check_function(args, expected, cls):
    (vocab, context, width, heads, depth), (batch, length, prefix, labelled) = args
    torch.manual_seed(44 + depth)
    model = cls(vocab, context, width, heads, depth)
    assert model.token.weight.shape == (vocab, width)
    assert model.position.weight.shape == (context, width)
    assert len({id(b) for b in model.blocks}) == depth
    assert isinstance(model.norm, nn.LayerNorm) and model.head.bias is None
    ids = torch.randint(vocab, (batch, prefix + length))
    x = model.token(ids) + model.position(torch.arange(prefix + length))
    oracle = []
    for block in model.blocks:
        assert isinstance(block, Block)
        x, kv = block(x)
        oracle.append(kv)
    want = model.head(model.norm(x))[:, prefix:]
    cache = [(k[:, :, :prefix], v[:, :, :prefix]) for k, v in oracle] if prefix else None
    targets = torch.randint(vocab, (batch, length)) if labelled else None
    got, loss, presents = model(ids[:, prefix:], targets, cache)
    torch.testing.assert_close(got, want, atol=2e-6, rtol=1e-5)
    assert len(presents) == depth
    for (k, v), (wk, wv) in zip(presents, oracle):
        torch.testing.assert_close(k, wk, atol=2e-6, rtol=1e-5)
        torch.testing.assert_close(v, wv, atol=2e-6, rtol=1e-5)
    if labelled:
        torch.testing.assert_close(loss, F.cross_entropy(want.flatten(0, 1), targets.flatten()))
        loss.backward()
        assert all(p.grad is not None for p in model.parameters())
    else:
        assert loss is None
    return True
