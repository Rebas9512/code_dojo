def valid_length(s: str) -> int:
    ends = [0] * len(s)
    best = 0
    for i in range(1, len(s)):
        if s[i] == ")":
            opening = i - ends[i - 1] - 1
            if opening >= 0 and s[opening] == "(":
                ends[i] = ends[i - 1] + 2
                if opening > 0:
                    ends[i] += ends[opening - 1]
                best = max(best, ends[i])
    return best
