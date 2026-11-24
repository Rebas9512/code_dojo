def check_function(args, expected, cls):
    (width, heads), (batch, length, prefix) = args
    torch.manual_seed(72 + prefix)
    layer = cls(width, heads)
    if layer.qkv.bias is not None or layer.proj.bias is not None:
        return False
    whole = torch.randn(batch, prefix + length, width, requires_grad=True)
    q, k, v = layer.qkv(whole).chunk(3, dim=-1)
    def split(t):
        return t.unflatten(-1, (heads, width // heads)).transpose(1, 2)
    q, k, v = split(q), split(k), split(v)
    mixed = F.scaled_dot_product_attention(q, k, v, is_causal=True)
    want = layer.proj(mixed.transpose(1, 2).flatten(2))[:, prefix:]
    past = (k[:, :, :prefix], v[:, :, :prefix]) if prefix else None
    got, (got_k, got_v) = layer(whole[:, prefix:], past)
    torch.testing.assert_close(got_k, k)
    torch.testing.assert_close(got_v, v)
    torch.testing.assert_close(got, want, atol=1e-6, rtol=1e-5)
    got.sum().backward()
    return all(p.grad is not None for p in layer.parameters())
