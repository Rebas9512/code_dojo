def train_one_epoch(model, loader, optimizer, loss_fn, max_norm):
    from torch.nn.utils import clip_grad_norm_

    model.train()
    loss_sum = 0.0
    sample_count = 0
    for features, labels in loader:
        optimizer.zero_grad()
        loss = loss_fn(model(features), labels)
        loss.backward()
        clip_grad_norm_(model.parameters(), max_norm)
        optimizer.step()
        loss_sum += loss.item() * len(labels)
        sample_count += len(labels)
    return loss_sum / sample_count
