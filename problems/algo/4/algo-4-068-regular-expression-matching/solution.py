from functools import cache


def matches(s: str, pattern: str) -> bool:
    @cache
    def match(i, j):
        if j == len(pattern):
            return i == len(s)
        first = i < len(s) and (pattern[j] == "." or pattern[j] == s[i])
        if j + 1 < len(pattern) and pattern[j + 1] == "*":
            return match(i, j + 2) or (first and match(i + 1, j))
        return first and match(i + 1, j + 1)

    return match(0, 0)
