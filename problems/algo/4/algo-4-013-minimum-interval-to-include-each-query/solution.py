import heapq


def shortest_cover(intervals: list[list[int]], queries: list[int]) -> list[int]:
    ordered = sorted(intervals)
    heap = []
    answer = [-1] * len(queries)
    i = 0
    for pos in sorted(range(len(queries)), key=lambda j: queries[j]):
        q = queries[pos]
        while i < len(ordered) and ordered[i][0] <= q:
            start, end = ordered[i]
            heapq.heappush(heap, (end - start + 1, end))
            i += 1
        while heap and heap[0][1] < q:
            heapq.heappop(heap)
        if heap:
            answer[pos] = heap[0][0]
    return answer
