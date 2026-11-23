def train(model, data, optimizer, steps):
    features, labels = data.train
    for _ in range(steps):
        scores = model(features)
        loss = data.loss(scores.softmax(dim=1), labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
