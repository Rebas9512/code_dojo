def interleaves(a: str, b: str, text: str) -> bool:
    if len(a) + len(b) != len(text):
        return False
    ok = [[False] * (len(b) + 1) for _ in range(len(a) + 1)]
    ok[0][0] = True
    for i in range(len(a) + 1):
        for j in range(len(b) + 1):
            if i and a[i - 1] == text[i + j - 1]:
                ok[i][j] = ok[i][j] or ok[i - 1][j]
            if j and b[j - 1] == text[i + j - 1]:
                ok[i][j] = ok[i][j] or ok[i][j - 1]
    return ok[-1][-1]
