def main():
    import argparse
    import json
    import torch
    from torch.nn import CrossEntropyLoss

    defaults = Config()
    parser = argparse.ArgumentParser(description="Train an MLP on handwritten digits")
    parser.add_argument("--epochs", type=int, default=defaults.epochs)
    parser.add_argument("--seed", type=int, default=defaults.seed)
    parser.add_argument("--batch-size", type=int, default=defaults.batch_size)
    parser.add_argument("--patience", type=int, default=defaults.patience)
    parser.add_argument("--checkpoint", default="best.pt")
    args = parser.parse_args()
    config = Config(seed=args.seed, epochs=args.epochs, batch_size=args.batch_size,
                    patience=args.patience)
    config.set_seed()
    torch.set_num_threads(1)
    dataset = DigitsDataset(DATA_DIR / "digits.csv")
    train_loader, valid_loader = make_loaders(
        dataset, round(len(dataset) * 0.2), config.batch_size, config.seed
    )
    model = build_model(config.hidden_size)
    optimizer, scheduler = make_optimizer(model, config)
    loss_fn = CrossEntropyLoss()
    stopping = EarlyStopping(config.patience, Checkpoint(args.checkpoint))

    for epoch in range(1, config.epochs + 1):
        lr = optimizer.param_groups[0]["lr"]
        loss = train_one_epoch(model, train_loader, optimizer, loss_fn, config.max_norm)
        accuracy = evaluate(model, valid_loader)
        print(json.dumps(epoch_record(epoch, loss, accuracy, lr)))
        scheduler.step()
        if stopping.observe(epoch, accuracy, model, optimizer):
            break

    best_epoch = stopping.restore(model, optimizer)
    accuracy = evaluate(model, valid_loader)
    print(json.dumps({"best_epoch": best_epoch, "val_accuracy": accuracy}))
