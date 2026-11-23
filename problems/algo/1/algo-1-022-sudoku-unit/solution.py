def has_conflict(board: list[list[str]], r: int, c: int) -> bool:
    digit = board[r][c]
    for row in range(9):
        for col in range(9):
            if (row, col) == (r, c):
                continue
            same_box = row // 3 == r // 3 and col // 3 == c // 3
            if (row == r or col == c or same_box) and board[row][col] == digit:
                return True
    return False
