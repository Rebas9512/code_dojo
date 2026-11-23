import copy
import torch
from dojo_train import assert_trajectory


def check_function(args, expected, fn):
    seed, steps, rate, decay, bound = args
    torch.manual_seed(seed)
    model = torch.nn.Linear(2, 1)
    reference = copy.deepcopy(model)
    x = torch.tensor([[1., 2.], [3., -2.], [-1., 1.]])
    y = torch.tensor([[2.], [-1.], [3.]])
    actual = fn(model, x, y, steps, rate, decay, bound)
    assert isinstance(actual, list) and len(actual) == steps and all(type(v) is float for v in actual), "每轮保存一个实际用于反向的浮点 loss"
    optimizer = torch.optim.Adam(reference.parameters(), lr=rate, weight_decay=decay)
    wanted = []
    for epoch in range(steps):
        optimizer.param_groups[0]["lr"] = rate * 0.5 ** (epoch // 2)
        optimizer.zero_grad()
        loss = (reference(x) - y).square().mean()
        wanted.append(loss.item())
        loss.backward()
        torch.nn.utils.clip_grad_norm_(reference.parameters(), bound)
        optimizer.step()
    assert_trajectory(actual, wanted)
    for actual_param, ref_param in zip(model.parameters(), reference.parameters()):
        assert torch.allclose(actual_param, ref_param, atol=1e-6), "末步参数不符，请检查裁剪、权重衰减和轮末步长"
    return True
