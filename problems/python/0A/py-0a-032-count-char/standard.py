def count_char(s: str, ch: str) -> int:
    count = 0
    for i in range(len(s)):
        if s[i] == ch:
            count += 1
    return count
