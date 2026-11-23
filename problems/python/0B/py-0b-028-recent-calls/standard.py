from collections import deque


class RecentCounter:
    def __init__(self):
        self.times = deque()

    def ping(self, t: int) -> int:
        self.times.append(t)
        cutoff = t - 3000
        while self.times[0] < cutoff:
            self.times.popleft()
        return len(self.times)
