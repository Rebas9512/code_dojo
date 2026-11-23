import torch
from torch import nn
from torch.nn import functional as F


class TinyDecoder(nn.Module):
    """单块解码器，用标准层和缩放点积算子产生对拍结果。"""

    def __init__(self, vocab=32, context=16, width=48, heads=4):
        super().__init__()
        self.heads = heads
        self.token = nn.Embedding(vocab, width)
        self.pos = nn.Embedding(context, width)
        self.n1 = nn.LayerNorm(width)
        self.qkv = nn.Linear(width, 3 * width, bias=False)
        self.proj = nn.Linear(width, width, bias=False)
        self.n2 = nn.LayerNorm(width)
        self.up = nn.Linear(width, 2 * width, bias=False)
        self.down = nn.Linear(2 * width, width, bias=False)
        self.final = nn.LayerNorm(width)
        self.readout = nn.Linear(width, vocab, bias=False)
        self.calls = []

    def project(self, ids, start):
        self.calls.append((start, ids.tolist()))
        batch, length = ids.shape
        x = self.token(ids) + self.pos(torch.arange(start, start + length))
        packed = self.qkv(self.n1(x)).unflatten(-1, (3, self.heads, -1))
        q, k, v = packed.permute(2, 0, 3, 1, 4).unbind(0)
        return x, q, k, v

    def finish(self, x, mixed):
        y = x + self.proj(mixed.transpose(1, 2).flatten(2))
        z = y + self.down(F.gelu(self.up(self.n2(y))))
        return self.readout(self.final(z))

    def forward(self, ids):
        x, q, k, v = self.project(ids, 0)
        mixed = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.finish(x, mixed)




def check_function(args, expected, fn):
    seed, prompt, steps = args
    torch.manual_seed(seed)
    model = TinyDecoder().eval()
    with torch.no_grad():
        want = list(prompt)
        for _ in range(steps):
            scores = model(torch.tensor([want]))[0, -1]
            want.append(int(torch.argmax(scores)))
        model.calls.clear()
        got = fn(model, prompt[:], steps)
        assert got == want, f"无缓存生成 {want}，实际为 {got}"
        calls = [(0, [prompt])] if steps else []
        calls += [(i, [[want[i]]]) for i in range(len(prompt), len(want)-1)]
        assert model.calls == calls, "首轮只投影提示；其后每轮只投影一个新词，且位置须连续"
    return True
