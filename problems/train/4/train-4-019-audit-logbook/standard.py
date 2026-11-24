import torch


def train(model, data, optimizer, steps):
    history = []
    for group in optimizer.param_groups:
        group["lr"] = 0.25
    generator = torch.Generator().manual_seed(0)
    x, y = data.train
    for _ in range(steps):
        order = torch.randperm(len(x), generator=generator)
        features, labels = x[order], y[order]
        scores = model(features)
        loss = data.loss(scores, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        history.append(loss.item())
    return history
