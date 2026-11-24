def solve(board: list[list[str]]) -> None:
    digits = set("123456789")
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []
    for r in range(9):
        for c in range(9):
            value = board[r][c]
            b = 3 * (r // 3) + c // 3
            if value == ".":
                empty.append((r, c, b))
            else:
                rows[r].add(value)
                cols[c].add(value)
                boxes[b].add(value)

    def fill(pos):
        if pos == len(empty):
            return True
        fewest = 10
        for j in range(pos, len(empty)):
            r, c, b = empty[j]
            possible = digits - rows[r] - cols[c] - boxes[b]
            if len(possible) < fewest:
                chosen, options, fewest = j, possible, len(possible)
                if fewest <= 1:
                    break
        empty[pos], empty[chosen] = empty[chosen], empty[pos]
        r, c, b = empty[pos]
        for value in sorted(options):
            board[r][c] = value
            rows[r].add(value)
            cols[c].add(value)
            boxes[b].add(value)
            if fill(pos + 1):
                return True
            rows[r].remove(value)
            cols[c].remove(value)
            boxes[b].remove(value)
            board[r][c] = "."
        empty[pos], empty[chosen] = empty[chosen], empty[pos]
        return False

    fill(0)


def run_case(board: list[list[str]]) -> list[list[str]]:
    solve(board)
    return board
