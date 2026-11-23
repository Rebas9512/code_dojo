import torch


def run_trial(model, x, y, steps, rate, decay, bound):
    optimizer = torch.optim.Adam(model.parameters(), lr=rate, weight_decay=decay)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.5)
    losses = []
    for _ in range(steps):
        prediction = model(x)
        loss = torch.mean((prediction - y) ** 2)
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), bound)
        optimizer.step()
        scheduler.step()
        losses.append(loss.item())
    return losses
