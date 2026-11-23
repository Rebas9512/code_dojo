from io import BytesIO
import torch

def check_function(args, expected, fn):
    seed = args[0]
    torch.manual_seed(seed)
    old, new = torch.nn.Linear(2, 1), torch.nn.Linear(2, 1)
    opt = torch.optim.SGD(old.parameters(), lr=0.2, momentum=0.8)
    fresh = torch.optim.SGD(new.parameters(), lr=0.01, momentum=0.1)
    def step(model, optimizer):
        optimizer.zero_grad()
        model(torch.tensor([1., 3.])).sum().backward()
        optimizer.step()
    step(old, opt)
    buf = BytesIO()
    torch.save(dict(model=old.state_dict(), optimizer=opt.state_dict(), epoch=seed+1), buf)
    epoch = fn(buf, new, fresh)
    assert epoch == seed+1, "应返回快照里记录的已完成轮数"
    for a,b in zip(old.parameters(),new.parameters()):
        assert torch.equal(a,b), "恢复后权重或偏置不符"
    step(old,opt)
    step(new,fresh)
    assert all(torch.allclose(a,b) for a,b in zip(old.parameters(),new.parameters())), "续走一步后参数不同，请恢复优化器的步长和缓冲"
    return True
