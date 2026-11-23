import torch


def check_function(args, expected, fn):
    table, prompt, temp, k, p, eos, limit, seed = args
    rng = torch.Generator().manual_seed(seed)
    want = list(prompt)
    while len(want) < len(prompt) + limit and want[-1] != eos:
        z = torch.tensor(table[want[-1]], dtype=torch.float64) / temp
        ranked = sorted(range(len(z)), key=lambda i: (-z[i].item(), i))[:k]
        first = torch.full_like(z, float("-inf"))
        first[ranked] = z[ranked]
        probs = torch.softmax(first, dim=0)
        total, keep = 0., []
        for i in ranked:
            total += float(probs[i])
            keep.append(i)
            if total >= p:
                break
        last = torch.full_like(z, float("-inf"))
        last[keep] = z[keep]
        want.append(int(torch.multinomial(torch.softmax(last, dim=0), 1, generator=rng)))
    got = fn(*args)
    assert got == want, f"期望生成 {want}，实际为 {got}"
    return True
