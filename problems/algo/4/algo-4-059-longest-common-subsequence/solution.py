def lcs_length(a: str, b: str) -> int:
    previous = [0] * (len(b) + 1)
    for x in a:
        row = [0]
        for j, y in enumerate(b, 1):
            if x == y:
                row.append(previous[j - 1] + 1)
            else:
                row.append(max(previous[j], row[-1]))
        previous = row
    return previous[-1]
