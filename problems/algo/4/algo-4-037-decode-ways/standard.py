def decode_count(s: str) -> int:
    two, one = 1, int(s[0] != "0")
    for i in range(1, len(s)):
        ways = one if s[i] != "0" else 0
        if "10" <= s[i - 1 : i + 1] <= "26":
            ways += two
        two, one = one, ways
    return one
