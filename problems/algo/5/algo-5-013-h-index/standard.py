def h_index(citations: list[int]) -> int:
    n = len(citations)
    buckets = [0] * (n + 1)
    for value in citations:
        buckets[min(n, value)] += 1
    count = 0
    for h in range(n, 0, -1):
        count += buckets[h]
        if count >= h:
            return h
    return 0
