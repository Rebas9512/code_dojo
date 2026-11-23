def count_queens(n: int) -> int:
    def place(row, columns, down, up):
        if row == n:
            return 1
        count = 0
        for col in range(n):
            if col not in columns and row-col not in down and row+col not in up:
                count += place(row + 1, columns.union({col}), down.union({row-col}), up.union({row+col}))
        return count
    return place(0, set(), set(), set())
