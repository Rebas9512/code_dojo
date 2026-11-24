def check_function(args, expected, fn):
    values, temperature, k, seed = args
    logits = torch.tensor(values, dtype=torch.float64)
    keep = sorted(range(len(values)), key=lambda i: (-values[i], i))[:k]
    scores = torch.full_like(logits, -torch.inf)
    scores[keep] = logits[keep] / temperature
    probabilities = scores.softmax(dim=0)
    rng = torch.Generator().manual_seed(seed)
    oracle = torch.Generator().manual_seed(seed)
    for _ in range(32):
        want = torch.multinomial(probabilities, 1, generator=oracle).item()
        actual = fn(logits, temperature, k, rng)
        assert type(actual) is int and actual == want, "检查筛选、温度、编号顺序和随机状态"
    assert torch.equal(rng.get_state(), oracle.get_state()), "每抽一次都应推进传入的随机状态"
    return logits.tolist() == values
