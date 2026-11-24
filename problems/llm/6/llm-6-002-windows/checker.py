def check_function(args, expected, cls):
    (ids,), (split, batch, length, seed) = args
    data = cls(ids)
    tokens = torch.tensor(ids)
    cut = 9 * len(ids) // 10
    if not torch.equal(data.train, tokens[:cut]) or not torch.equal(data.valid, tokens[cut:]):
        return False
    seq = tokens[:cut] if split == "train" else tokens[cut:]
    rng = torch.Generator().manual_seed(seed)
    oracle = torch.Generator().manual_seed(seed)
    for _ in range(2):
        starts = torch.randint(len(seq) - length, (batch,), generator=oracle).tolist()
        x, y = data.get_batch(split, batch, length, rng)
        want_x = torch.stack([seq[i:i + length] for i in starts])
        want_y = torch.stack([seq[i + 1:i + length + 1] for i in starts])
        if x.dtype != torch.long or y.dtype != torch.long:
            return False
        if not torch.equal(x, want_x) or not torch.equal(y, want_y):
            return False
    return True
