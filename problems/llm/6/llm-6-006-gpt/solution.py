class GPT(nn.Module):
    def __init__(self, vocab_size, context, width, heads, layers):
        nn.Module.__init__(self)
        self.token = nn.Embedding(vocab_size, width)
        self.position = nn.Embedding(context, width)
        self.blocks = nn.ModuleList([Block(width, heads) for _ in range(layers)])
        self.norm = nn.LayerNorm(width)
        self.head = nn.Linear(width, vocab_size, bias=False)

    def forward(self, ids, targets=None, cache=None):
        length = ids.size(1)
        start = 0 if cache is None else cache[0][0].size(2)
        x = self.token(ids) + self.position(torch.arange(start, start + length))
        presents = []
        for i, block in enumerate(self.blocks):
            past = None if cache is None else cache[i]
            x, present = block(x, past)
            presents.append(present)
        logits = self.head(self.norm(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.flatten(0, 1), targets.flatten())
        return logits, loss, presents
