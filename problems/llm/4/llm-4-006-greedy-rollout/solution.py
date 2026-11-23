def greedy_rollout(table, prompt, steps):
    tokens = list(prompt)
    for _ in range(steps):
        row: list = table[tokens[-1]]
        tokens.append(row.index(max(row)))
    return tokens
