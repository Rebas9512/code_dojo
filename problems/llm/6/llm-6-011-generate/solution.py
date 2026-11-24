@torch.no_grad()
def generate(model, prompt, steps, temperature, k, seed, use_cache):
    generator = torch.Generator().manual_seed(seed)
    result = list(prompt)
    ids = torch.tensor([result])
    cache = None
    for _ in range(steps):
        logits, _, present = model(ids, cache=cache)
        token = sample_token(logits[0, -1], temperature, k, generator)
        result.append(token)
        if use_cache:
            cache = present
            ids = torch.tensor([[token]])
        else:
            ids = torch.tensor([result])
    return result
