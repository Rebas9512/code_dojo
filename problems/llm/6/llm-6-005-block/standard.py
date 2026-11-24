class Block(nn.Module):
    def __init__(self, width, heads):
        nn.Module.__init__(self)
        self.norm1 = nn.LayerNorm(width)
        self.attention = CausalAttention(width, heads)
        self.norm2 = nn.LayerNorm(width)
        self.mlp = build_mlp(width)

    def forward(self, x, past=None):
        update, present = self.attention(self.norm1(x), past)
        x = x + update
        return x + self.mlp(self.norm2(x)), present
