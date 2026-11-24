def check_function(args, expected, cls):
    (width, heads), (batch, length, prefix) = args
    torch.manual_seed(31 + prefix)
    block = cls(width, heads)
    assert block.norm1 is not block.norm2
    assert all(isinstance(n, nn.LayerNorm) and n.normalized_shape == (width,)
               for n in (block.norm1, block.norm2))
    assert isinstance(block.attention, CausalAttention)
    past = None
    if prefix:
        history = torch.randn(batch, prefix, width)
        _, past = block.attention(block.norm1(history))
    x = torch.randn(batch, length, width)
    branch, (keys, values) = block.attention(block.norm1(x), past)
    middle = x + branch
    want = middle + block.mlp(block.norm2(middle))
    got, (got_k, got_v) = block(x, past)
    torch.testing.assert_close(got, want)
    torch.testing.assert_close(got_k, keys)
    torch.testing.assert_close(got_v, values)
    got.sum().backward()
    return all(p.grad is not None for p in block.parameters())
