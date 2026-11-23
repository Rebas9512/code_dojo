def update(model, data, optimizer):
    x, y = data.train
    scores = model(x)
    loss = data.loss(scores, y)
    optimizer.zero_grad()
    loss.backward()
    ____  # 在此补全
