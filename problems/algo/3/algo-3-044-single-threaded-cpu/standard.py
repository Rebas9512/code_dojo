import heapq


def execution_order(tasks: list[list[int]]) -> list[int]:
    waiting = sorted((start, cost, i) for i, (start, cost) in enumerate(tasks))
    heap, order = [], []
    time = index = 0
    while heap or index < len(waiting):
        if not heap:
            time = max(time, waiting[index][0])
        while index < len(waiting) and waiting[index][0] <= time:
            start, cost, i = waiting[index]
            heapq.heappush(heap, (cost, i))
            index += 1
        cost, i = heapq.heappop(heap)
        order.append(i)
        time += cost
    return order
