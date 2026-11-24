from collections import Counter


def has_word(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    counts = Counter(ch for row in board for ch in row)
    if any(counts[ch] < count for ch, count in Counter(word).items()):
        return False
    if counts[word[-1]] < counts[word[0]]:
        word = word[::-1]

    def match(r, c, index):
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[index]:
            return False
        if index + 1 == len(word):
            return True
        saved = board[r][c]
        board[r][c] = ''
        found = any(
            match(r + dr, c + dc, index + 1) for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0))
        )
        board[r][c] = saved
        return found

    return any(match(r, c, 0) for r in range(rows) for c in range(cols))
