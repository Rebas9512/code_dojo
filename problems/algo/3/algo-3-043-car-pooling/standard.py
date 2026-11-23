import heapq


def fits(trips: list[list[int]], capacity: int) -> bool:
    onboard = []
    riding = 0
    for people, start, stop in sorted(trips, key=lambda trip: trip[1]):
        while onboard and onboard[0][0] <= start:
            _, leaving = heapq.heappop(onboard)
            riding -= leaving
        riding += people
        if riding > capacity:
            return False
        heapq.heappush(onboard, (stop, people))
    return True
