def queen_boards(n: int) -> list[list[str]]:
    result, columns = [], []
    used, down, up = set(), set(), set()
    def place(row):
        if row == n:
            result.append(['.' * col + 'Q' + '.' * (n-col-1) for col in columns])
            return
        for col in range(n):
            if col in used or row-col in down or row+col in up:
                continue
            used.add(col)
            down.add(row-col)
            up.add(row+col)
            columns.append(col)
            place(row + 1)
            columns.pop()
            used.remove(col)
            down.remove(row-col)
            up.remove(row+col)
    place(0)
    return result
