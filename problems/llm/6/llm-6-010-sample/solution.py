def sample_token(logits, temperature, k, generator):
    order = torch.argsort(logits, descending=True, stable=True)
    scores = logits / temperature
    scores[order[k:]] = float("-inf")
    probabilities = torch.softmax(scores, dim=0)
    return torch.multinomial(probabilities, 1, generator=generator).item()
