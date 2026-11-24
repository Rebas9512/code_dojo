def advance(board: list[list[int]]) -> None:
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            count = 0
            for i in range(max(0, r - 1), min(rows, r + 2)):
                for j in range(max(0, c - 1), min(cols, c + 2)):
                    if (i, j) != (r, c):
                        count += board[i][j] & 1
            if count == 3 or (count == 2 and board[r][c]):
                board[r][c] |= 2
    for row in board:
        for j in range(cols):
            row[j] >>= 1


def run_case(board: list[list[int]]) -> list[list[int]]:
    advance(board)
    return board
