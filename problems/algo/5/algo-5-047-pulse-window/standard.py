from collections import deque


class PulseCounter:
    def __init__(self):
        self.times = deque()
        self.counts = {}
        self.total = 0

    def hit(self, time: int) -> None:
        self._expire(time)
        if time not in self.counts:
            self.times.append(time)
            self.counts[time] = 0
        self.counts[time] += 1
        self.total += 1

    def count(self, time: int) -> int:
        self._expire(time)
        return self.total

    def _expire(self, time):
        while self.times and self.times[0] <= time - 300:
            expired = self.times.popleft()
            self.total -= self.counts.pop(expired)
