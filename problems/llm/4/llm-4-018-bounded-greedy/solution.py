def generate(table, prompt, eos, limit):
    out = list(prompt)
    for _ in range(limit):
        if out[-1] == eos:
            break
        scores: list = table[out[-1]]
        out.append(scores.index(max(scores)))
    return out
