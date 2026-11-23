import torch


def train(model, data, optimizer, steps):
    features, labels = data.train
    for _ in range(steps):
        scores = model(features)
        loss = data.loss(scores, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    model.eval()
    with data.evaluating():
        model(data.valid[0])
