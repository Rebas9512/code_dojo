def triangle(rows: int) -> list[list[int]]:
    result = [[1]]
    for i in range(1, rows):
        previous = result[-1]
        row = [1]
        for j in range(1, i):
            row.append(previous[j - 1] + previous[j])
        row.append(1)
        result.append(row)
    return result
