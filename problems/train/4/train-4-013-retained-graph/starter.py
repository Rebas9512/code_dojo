def train(model, data, optimizer, steps):
    history = []
    features, labels = data.train
    for _ in range(steps):
        scores = model(features)
        loss = data.loss(scores, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        history.append(loss)
    return history
