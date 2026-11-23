def train(model, data, optimizer, steps):
    for group in optimizer.param_groups:
        group["lr"] = 25.0
    features, labels = data.train
    for _ in range(steps):
        scores = model(features)
        loss = data.loss(scores, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
