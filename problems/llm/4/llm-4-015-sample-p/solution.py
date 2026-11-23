import torch


def draw(probabilities, count, seed):
    generator = torch.Generator().manual_seed(seed)
    return [torch.multinomial(probabilities, 1, generator=generator).item() for _ in range(count)]


def nucleus(probs, p):
    order = sorted(range(len(probs)), key=lambda i: (-probs[i], i))
    mass = 0.0
    kept = []
    for i in order:
        kept.append(i)
        mass += probs[i]
        if mass >= p:
            break
    return kept


def sample_p(scores, p, count, seed):
    z = torch.tensor(scores, dtype=torch.float64)
    keep = nucleus(torch.softmax(z, dim=0).tolist(), p)
    filtered = torch.full_like(z, float("-inf"))
    filtered[keep] = z[keep]
    return draw(torch.softmax(filtered, dim=0), count, seed)
