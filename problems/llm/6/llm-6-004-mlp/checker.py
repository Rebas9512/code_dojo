def check_function(args, expected, fn):
    width, batch, length = args
    torch.manual_seed(9 + width)
    mlp = fn(width)
    up, down = [layer for layer in mlp.modules() if isinstance(layer, nn.Linear)]
    assert (up.in_features, up.out_features) == (width, 4 * width), "第一层应扩到四倍宽"
    assert (down.in_features, down.out_features) == (4 * width, width), "第二层应还原宽度"
    assert up.bias is not None and down.bias is not None, "两层都需要偏置"
    x = torch.randn(batch, length, width)
    got = mlp(x)
    torch.testing.assert_close(got, down(F.gelu(up(x))))
    got.sum().backward()
    return all(p.grad is not None for p in mlp.parameters())
