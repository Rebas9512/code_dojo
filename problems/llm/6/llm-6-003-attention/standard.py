class CausalAttention(nn.Module):
    def __init__(self, width, heads):
        nn.Module.__init__(self)
        self.heads = heads
        self.qkv = nn.Linear(width, 3 * width, bias=False)
        self.proj = nn.Linear(width, width, bias=False)

    def forward(self, x, past=None):
        batch, length, width = x.shape
        depth = width // self.heads
        packed = self.qkv(x).reshape(batch, length, 3, self.heads, depth)
        q, k, v = packed.permute(2, 0, 3, 1, 4).unbind(0)
        if past is not None:
            k = torch.cat((past[0], k), dim=2)
            v = torch.cat((past[1], v), dim=2)

        total = k.size(2)
        query_pos = torch.arange(total - length, total)
        future = torch.arange(total)[None, :] > query_pos[:, None]
        scores = q @ k.transpose(-2, -1) / math.sqrt(depth)
        weights = scores.masked_fill(future, float("-inf")).softmax(dim=-1)
        mixed = (weights @ v).transpose(1, 2).reshape(batch, length, width)
        return self.proj(mixed), (k, v)
