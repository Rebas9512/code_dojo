from collections import defaultdict, deque


class ChannelCounter:
    def __init__(self, width: int):
        self.width = width
        self.events = defaultdict(deque)

    def _expire(self, events, time):
        while events and events[0] <= time - self.width:
            events.popleft()

    def hit(self, channel: str, time: int) -> None:
        events = self.events[channel]
        self._expire(events, time)
        events.append(time)

    def count(self, channel: str, time: int) -> int:
        events = self.events.get(channel)
        if not events:
            return 0
        self._expire(events, time)
        return len(events)
