def projection_counts(prompt_len, steps):
    if steps == 0:
        return [0, 0]
    full = sum(range(prompt_len, prompt_len + steps))
    cached = prompt_len + steps - 1
    return [full, cached]
