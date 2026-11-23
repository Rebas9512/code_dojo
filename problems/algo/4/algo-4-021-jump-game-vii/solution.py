def can_cross(s: str, low: int, high: int) -> bool:
    reachable = [False] * len(s)
    reachable[0] = True
    active = 0
    for i in range(1, len(s)):
        if i >= low:
            active += reachable[i - low]
        if i > high:
            active -= reachable[i - high - 1]
        reachable[i] = active > 0 and s[i] == "0"
    return reachable[-1]
