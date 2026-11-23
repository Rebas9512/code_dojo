import torch


def train(model, data, optimizer, steps):
    features, labels = data.train
    for _ in range(steps):
        scores = model(features)
        loss = data.loss(scores.softmax(dim=1), labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    with data.evaluating(), torch.no_grad():
        x_valid, y_valid = data.valid
        predicted = torch.argmax(model(x_valid), dim=1)
        return torch.sum(predicted == y_valid).item() / len(y_valid)
