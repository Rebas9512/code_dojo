import torch


def train(model, data, optimizer, steps):
    optimizer.zero_grad()
    for _ in range(steps):
        x, y = data.train
        loss = data.loss(model(x), y)
        loss.backward()
        optimizer.step()
    model.eval()
    with data.evaluating(), torch.no_grad():
        model(data.valid[0])
