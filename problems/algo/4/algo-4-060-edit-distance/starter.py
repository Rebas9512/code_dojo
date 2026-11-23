def edit_steps(a: str, b: str) -> int:
    previous = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        row = [0]
        for j, y in enumerate(b, 1):
            row.append(min(previous[j] + 1, row[-1] + 1,
                           previous[j - 1] + (x != y)))
        previous = row
    return previous[-1]
