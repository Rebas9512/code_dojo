import torch


def check_function(args, expected, cls):
    patience, scores = args[0]
    model = torch.nn.Linear(1, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
    stop = cls(patience, Checkpoint("early.pt"))
    highest = -1.0
    best_epoch = 0
    for epoch, accuracy in enumerate(scores, 1):
        with torch.no_grad():
            model.weight.fill_(epoch)
            model.bias.fill_(-epoch)
        optimizer.param_groups[0]["lr"] = epoch / 10
        if accuracy > highest:
            highest, best_epoch = accuracy, epoch
        should_stop = stop.observe(epoch, accuracy, model, optimizer)
        assert should_stop is (epoch - best_epoch >= patience), "应返回是否已连续等待指定轮数的布尔值"
        if should_stop:
            break
    last, best = expected
    assert epoch == last, "持平也计入等待，严格刷新最高值后等待数归零"
    # 即使最后一轮就是最佳轮，也要能从独立快照恢复。
    with torch.no_grad():
        model.weight.zero_()
    restored = stop.restore(model, optimizer)
    assert restored == best, "恢复后应返回首次最佳轮的轮号"
    assert model.weight.item() == best and model.bias.item() == -best, "请恢复最佳轮的全部模型参数"
    assert optimizer.param_groups[0]["lr"] == best / 10, "模型和优化器应恢复到同一轮"
    return True
