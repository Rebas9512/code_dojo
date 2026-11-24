import torch
import torch.nn.functional as F


def normalize(values, state, name):
    width = values.shape[-1]
    return F.layer_norm(values, (width,), state[name + ".weight"], state[name + ".bias"])


def gpt_logits(ids, state):
    batch, length = ids.shape
    x = state["token.weight"][ids] + state["pos.weight"][:length]
    width = x.shape[-1]
    depth = width // 4

    qkv = F.linear(normalize(x, state, "n1"), state["qkv.weight"])
    q, k, v = [
        part.reshape(batch, length, 4, depth).transpose(1, 2)
        for part in torch.chunk(qkv, 3, dim=-1)
    ]
    scores = q @ k.transpose(-2, -1) / depth**0.5
    future = torch.triu(torch.ones(length, length, dtype=torch.bool), diagonal=1)
    mixed = torch.softmax(scores.masked_fill(future, float("-inf")), dim=-1) @ v
    words = mixed.transpose(1, 2).reshape(batch, length, width)
    y = x + F.linear(words, state["proj.weight"])
    hidden = F.gelu(F.linear(normalize(y, state, "n2"), state["up.weight"]))
    z = y + F.linear(hidden, state["down.weight"])
    return F.linear(normalize(z, state, "final"), state["readout.weight"])
