def batch_savings(jobs):
    saved = 0
    for prompt_len, steps in jobs:
        for length in range(prompt_len, prompt_len + steps - 1):
            saved += length * (length + 1) // 2
    return saved
