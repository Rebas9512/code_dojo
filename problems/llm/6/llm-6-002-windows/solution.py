class TextWindows:
    def __init__(self, ids):
        tokens = torch.tensor(ids, dtype=torch.long)
        cut = 9 * len(ids) // 10
        self.train = tokens[:cut]
        self.valid = tokens[cut:]

    def get_batch(self, split, batch_size, context, generator):
        tokens = self.train if split == "train" else self.valid
        starts = torch.randint(len(tokens) - context, (batch_size,), generator=generator)
        positions = starts[:, None] + torch.arange(context)
        return tokens[positions], tokens[positions + 1]
