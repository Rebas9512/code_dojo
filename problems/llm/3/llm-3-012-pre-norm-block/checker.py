import torch
import torch.nn.functional as F
from dojo_compare import allclose


def check_function(args, expected, fn):
    torch.manual_seed(args[0])
    x = torch.randn(2, 3, 4)
    norm1, norm2 = torch.nn.LayerNorm(4), torch.nn.LayerNorm(4)
    with torch.no_grad():
        norm2.bias.copy_(torch.randn(4))
        output = torch.nn.Linear(4, 4)
        def attention(z):
            q, k, v = [a.unsqueeze(1) for a in (z, z * 0.7, z)]
            return output(F.scaled_dot_product_attention(q, k, v, is_causal=True).squeeze(1))
        mlp = torch.nn.Sequential(torch.nn.Linear(4, 8), torch.nn.GELU(), torch.nn.Linear(8, 4))
        y = x + attention(norm1(x))
        want = y + mlp(norm2(y))
        why = allclose(want, fn(x.clone(), norm1, attention, norm2, mlp), rtol=1e-5, atol=1e-6)
    assert why is None, why
    return True
