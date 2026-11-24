import heapq


def cheap_pairs(a: list[int], b: list[int], k: int) -> list[list[int]]:
    heap = [(a[i] + b[0], i, 0) for i in range(min(k, len(a)))]
    out = []
    while len(out) < k:
        _, i, j = heapq.heappop(heap)
        out.append([a[i], b[j]])
        if j + 1 < len(b):
            heapq.heappush(heap, (a[i] + b[j + 1], i, j + 1))
    return out
