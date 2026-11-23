import torch


def sample_until(table, prompt, temperature, k, p, eos, limit, seed):
    tokens = list(prompt)
    rng = torch.Generator().manual_seed(seed)
    for _ in range(limit):
        if tokens[-1] == eos:
            break
        z = torch.tensor(table[tokens[-1]], dtype=torch.float64) / temperature
        order = torch.argsort(z, descending=True, stable=True)
        z[order[k:]] = float("-inf")
        probs = torch.softmax(z, dim=0)
        mass = 0.0
        for rank, index in enumerate(order[:k]):
            mass += probs[index].item()
            if mass >= p:
                z[order[rank + 1:]] = float("-inf")
                break
        token = torch.multinomial(torch.softmax(z, dim=0), 1, generator=rng).item()
        tokens.append(token)
    return tokens
