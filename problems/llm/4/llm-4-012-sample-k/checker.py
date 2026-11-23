import torch


def check_function(args, expected, fn):
    scores, cutoff, count, seed = args
    z = torch.tensor(scores, dtype=torch.float64)
    order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
    kept = order[:cutoff]
    masked = torch.tensor([scores[i] if i in kept else float("-inf") for i in range(len(scores))],
                          dtype=torch.float64)
    prob = torch.softmax(masked, dim=0)
    rng = torch.Generator().manual_seed(seed)
    want = [int(torch.multinomial(prob, 1, generator=rng)) for _ in range(count)]
    got = fn(scores[:], cutoff, count, seed)
    assert got == want, f"按原词表顺序抽样应得 {want}，实际为 {got}"
    return True
