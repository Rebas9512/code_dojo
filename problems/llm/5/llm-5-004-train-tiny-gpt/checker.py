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



from dojo_train import simulate_train, assert_loss_decreased, assert_trajectory


def batches():
    letters = {c: i for i, c in enumerate("abc")}
    stream = [letters[c] for c in "abcabcabcabc"]
    train = torch.tensor([stream[:7], stream[1:8], stream[2:9]])
    valid = torch.tensor([stream[3:10]])
    return (train[:, :-1], train[:, 1:]), (valid[:, :-1], valid[:, 1:])


def reference(model, data, optimizer, steps):
    x, y = data.train
    for _ in range(steps):
        optimizer.zero_grad()
        data.loss(model(x), y).backward()
        optimizer.step()


def check_function(args, expected, fn):
    settings = dict(make_model=lambda: TinyDecoder(vocab=3, context=8, width=12, heads=3),
                    make_data=batches, make_optimizer=lambda params: torch.optim.SGD(params, lr=0.18),
                    loss_fn=lambda z, y: F.cross_entropy(z.flatten(0, 1), y.flatten()),
                    steps=24, seed=args[0])
    losses = simulate_train(fn, require_eval=True, **settings)
    assert_loss_decreased(losses, window=5, ratio=0.5)
    assert_trajectory(losses, simulate_train(reference, **settings))
    return True
