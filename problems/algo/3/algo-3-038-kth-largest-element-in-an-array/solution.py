import heapq


def kth_largest(nums: list[int], k: int) -> int:
    heap = nums[:k]
    heapq.heapify(heap)
    for value in nums[k:]:
        if value > heap[0]:
            heapq.heapreplace(heap, value)
    return heap[0]
