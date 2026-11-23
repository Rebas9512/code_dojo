import heapq


def longest_string(a: int, b: int, c: int) -> str:
    heap = [(-count, char) for count, char in zip((a, b, c), 'abc') if count]
    heapq.heapify(heap)
    result = []
    while heap:
        count, char = heapq.heappop(heap)
        if len(result) >= 2 and result[-2] == result[-1] == char:
            if not heap:
                break
            other_count, other = heapq.heappop(heap)
            heapq.heappush(heap, (count, char))
            count, char = other_count, other
        result.append(char)
        if count < -1:
            heapq.heappush(heap, (count + 1, char))
    return ''.join(result)
