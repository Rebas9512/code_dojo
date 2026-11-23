def total_score(ops: list[str]) -> int:
    scores = []
    for op in ops:
        if op == 'C':
            scores.pop()
        elif op == 'D':
            scores.append(scores[-1] * 2)
        elif op == '+':
            scores.append(scores[-1] + scores[-2])
        else:
            scores.append(int(op))
    return sum(scores)
