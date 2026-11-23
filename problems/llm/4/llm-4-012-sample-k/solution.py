import torch


def draw(probabilities, count, seed):
    generator = torch.Generator().manual_seed(seed)
    return [torch.multinomial(probabilities, 1, generator=generator).item() for _ in range(count)]


def sample_k(scores, k, count, seed):
    z = torch.tensor(scores, dtype=torch.float64)
    order = torch.argsort(z, descending=True, stable=True)
    z[order[k:]] = float("-inf")
    return draw(torch.softmax(z, dim=0), count, seed)
