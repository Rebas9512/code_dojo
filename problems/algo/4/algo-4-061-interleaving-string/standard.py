def interleaves(a: str, b: str, text: str) -> bool:
    if len(a) + len(b) != len(text):
        return False
    possible = [True] + [False] * len(b)
    for j in range(1, len(b) + 1):
        possible[j] = possible[j - 1] and b[j - 1] == text[j - 1]
    for i in range(1, len(a) + 1):
        possible[0] = possible[0] and a[i - 1] == text[i - 1]
        for j in range(1, len(b) + 1):
            wanted = text[i + j - 1]
            possible[j] = (possible[j] and a[i - 1] == wanted) or (
                possible[j - 1] and b[j - 1] == wanted
            )
    return possible[-1]
