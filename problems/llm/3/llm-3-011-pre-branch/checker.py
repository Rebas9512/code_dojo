import torch
from dojo_compare import allclose


def check_function(args, expected, fn):
    torch.manual_seed(args[0])
    x = torch.randn(2, 3, 4)
    norm = torch.nn.LayerNorm(4)
    branch = torch.nn.Linear(4, 4)
    with torch.no_grad():
        want = x + branch(norm(x))
        reason = allclose(want, fn(x.clone(), norm, branch), rtol=1e-5, atol=1e-6)
    assert reason is None, reason
    return True
