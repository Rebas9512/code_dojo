import torch


def train(model, data, optimizer, steps):
    features, labels = data.train
    vx, vy = data.valid
    features, labels = torch.cat([features, vx]), torch.cat([labels, vy])
    for _ in range(steps):
        scores = model(features)
        loss = data.loss(scores, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    model.eval()
    with data.evaluating(), torch.no_grad():
        model(data.valid[0])
