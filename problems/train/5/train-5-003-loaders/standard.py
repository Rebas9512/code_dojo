def make_loaders(dataset, valid_size, batch_size, seed):
    import torch
    from torch.utils.data import DataLoader, random_split

    generator = torch.Generator().manual_seed(seed)
    valid, train = random_split(
        dataset, [valid_size, len(dataset) - valid_size], generator=generator
    )
    train_loader = DataLoader(train, batch_size=batch_size, shuffle=True, generator=generator)
    valid_loader = DataLoader(valid, batch_size=batch_size)
    return train_loader, valid_loader
