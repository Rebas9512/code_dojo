def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    root = {}
    for word in words:
        node = root
        for letter in word:
            node = node.setdefault(letter, {})
        node["#"] = word
    found = []
    rows, cols = len(board), len(board[0])

    def explore(r, c, parent):
        letter = board[r][c]
        if letter not in parent:
            return
        node = parent[letter]
        if "#" in node:
            found.append(node.pop("#"))
        board[r][c] = "!"
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                explore(nr, nc, node)
        board[r][c] = letter
        if not node:
            del parent[letter]

    for r in range(rows):
        for c in range(cols):
            explore(r, c, root)
    return found
