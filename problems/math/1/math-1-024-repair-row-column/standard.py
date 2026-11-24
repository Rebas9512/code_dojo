def multiply(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    result = []
    for row in a:
        line = []
        for c in range(len(b[0])):
            line.append(sum(row[k] * b[k][c] for k in range(len(row))))
        result.append(line)
    return result
