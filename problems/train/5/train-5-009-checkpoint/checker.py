from pathlib import Path

import torch


def check_function(args, expected, cls):
    epoch, steps = args[0]
    torch.manual_seed(epoch)
    model = torch.nn.Linear(2, 1)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.03)
    x = torch.tensor([[0.2, -0.4]])
    def step(m, opt):
        opt.zero_grad()
        m(x).square().sum().backward()
        opt.step()
    for _ in range(steps):
        step(model, optimizer)
    path = Path(f"epoch-{epoch}.pt")
    cls(path).save(model, optimizer, epoch)
    state = torch.load(path, weights_only=True)
    assert {"model", "optimizer", "epoch"} <= state.keys() and state["epoch"] == epoch, "检查点要能在磁盘上独立读取三个字段"
    other = torch.nn.Linear(2, 1)
    fresh = torch.optim.AdamW(other.parameters(), lr=0.9)
    assert cls(path).load(other, fresh) == epoch, "读取时返回保存的轮号"
    for m, opt in [(model, optimizer), (other, fresh)]:
        step(m, opt)
    for a, b in zip(model.parameters(), other.parameters()):
        assert torch.equal(a, b), "恢复后再走一个相同步骤，AdamW 的参数和动量应接得上"
    return True
