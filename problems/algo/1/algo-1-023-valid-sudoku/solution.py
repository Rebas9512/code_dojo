def is_valid_sudoku(board: list[list[str]]) -> bool:
    seen = set()
    for r in range(9):
        for c in range(9):
            digit = board[r][c]
            if digit == '.':
                continue
            box = r // 3 * 3 + c // 3
            for key in [('row', r, digit), ('column', c, digit), ('box', box, digit)]:
                if key in seen:
                    return False
                seen.add(key)
    return True
