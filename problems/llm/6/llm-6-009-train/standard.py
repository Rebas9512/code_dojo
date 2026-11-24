def train_model(model, data, optimizer, cfg):
    train_rng = torch.Generator().manual_seed(cfg.seed)
    history = []
    for step in range(cfg.steps + 1):
        if step > 0:
            model.train()
            lr = learning_rate(step, cfg.steps, cfg.warmup, cfg.peak, cfg.floor)
            for group in optimizer.param_groups:
                group["lr"] = lr
            x, y = data.get_batch("train", cfg.batch_size, cfg.context, train_rng)
            optimizer.zero_grad()
            _, loss, _ = model(x, y)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), cfg.clip)
            optimizer.step()

        if step % cfg.eval_every == 0 or step == cfg.steps:
            model.eval()
            valid_rng = torch.Generator().manual_seed(cfg.seed + 1)
            total = 0.0
            with torch.no_grad():
                for _ in range(cfg.eval_batches):
                    x, y = data.get_batch("valid", cfg.batch_size, cfg.context, valid_rng)
                    _, loss, _ = model(x, y)
                    total += loss.item()
            mean_loss = total / cfg.eval_batches
            history.append((step, mean_loss))
            print(f"step={step} val_loss={mean_loss:.4f}")
    return history
