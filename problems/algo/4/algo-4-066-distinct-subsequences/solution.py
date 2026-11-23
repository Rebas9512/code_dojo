def subseq_count(s: str, t: str) -> int:
    ways = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == ch:
                ways[j] += ways[j - 1]
    return ways[-1]
