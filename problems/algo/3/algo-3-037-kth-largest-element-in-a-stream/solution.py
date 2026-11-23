import heapq


class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = []
        for value in nums:
            self.add(value)

    def add(self, value: int) -> int:
        heapq.heappush(self.heap, value)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
