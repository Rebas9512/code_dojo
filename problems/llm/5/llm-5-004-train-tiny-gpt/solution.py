import torch


def train_lm(model, data, optimizer, steps):
    x, targets = data.train
    model.train()
    for _ in range(steps):
        optimizer.zero_grad()
        logits = model(x)
        data.loss(logits, targets).backward()
        optimizer.step()
    model.eval()
    with data.evaluating(), torch.no_grad():
        model(data.valid[0])
