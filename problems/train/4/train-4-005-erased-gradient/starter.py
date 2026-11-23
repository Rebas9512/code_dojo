import torch


def train(model, data, optimizer, steps):
    features, labels = data.train
    for _ in range(steps):
        scores = model(features)
        loss = data.loss(scores, labels)
        loss.backward()
        optimizer.zero_grad()
        optimizer.step()
    model.eval()
    with data.evaluating(), torch.no_grad():
        model(data.valid[0])
