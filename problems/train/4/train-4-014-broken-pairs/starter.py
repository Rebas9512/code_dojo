import torch


def train(model, data, optimizer, steps):
    generator = torch.Generator().manual_seed(0)
    x, y = data.train
    for _ in range(steps):
        order = torch.randperm(len(x), generator=generator)
        features, labels = x[order], y
        scores = model(features)
        loss = data.loss(scores, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
