from collections import deque


class PulseCounter:
    def __init__(self):
        self.events = deque()

    def hit(self, time: int) -> None:
        self._expire(time)
        self.events.append(time)

    def count(self, time: int) -> int:
        self._expire(time)
        return len(self.events)

    def _expire(self, time):
        while self.events and self.events[0] <= time - 300:
            self.events.popleft()
