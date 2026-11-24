def zigzag(text: str, rows: int) -> str:
    if rows == 1 or rows >= len(text):
        return text
    lines = [[] for _ in range(rows)]
    row, step = 0, 1
    for ch in text:
        lines[row].append(ch)
        if row == rows - 1:
            step = -1
        elif row == 0:
            step = 1
        row += step
    return "".join("".join(line) for line in lines)
