def hanoi(n: int, start: str, spare: str, end: str) -> list[str]:
    if n == 0:
        return []
    before = hanoi(n - 1, start, end, spare)
    move = [start + "→" + end]
    after = hanoi(n - 1, spare, start, end)
    return before + move + after
