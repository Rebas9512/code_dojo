import torch


def bounded_step(model, loss, optimizer, bound):
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), bound)
    optimizer.step()
