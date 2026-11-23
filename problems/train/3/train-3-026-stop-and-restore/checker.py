import torch


def check_function(args, expected, fn):
    losses, patience = args
    torch.manual_seed(0)
    model = torch.nn.Linear(1, 1)
    seen = []
    def epochs():
        for i, loss in enumerate(losses, 1):
            with torch.no_grad():
                model.weight.fill_(i * 2)
                model.bias.fill_(-i)
            seen.append(i)
            yield loss
    stop, best = expected
    answer = fn(model, epochs(), patience)
    assert len(seen) == stop, f"按连续未改善轮数，应读到第 {stop} 轮"
    assert answer == best, f"首次最佳验证轮应为第 {best} 轮"
    assert model.weight.item() == 2*best and model.bias.item() == -best, "请恢复最佳轮的完整快照，状态字典的浅引用会随模型变化"
    return True
