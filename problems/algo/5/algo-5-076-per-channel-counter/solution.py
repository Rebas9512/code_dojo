from collections import defaultdict, deque


class ChannelCounter:
    def __init__(self, width: int):
        self.width = width
        self.events = defaultdict(deque)

    def _expire(self, channel, time):
        events = self.events[channel]
        while events and events[0] <= time - self.width:
            events.popleft()
        return events

    def hit(self, channel: str, time: int) -> None:
        self._expire(channel, time).append(time)

    def count(self, channel: str, time: int) -> int:
        return len(self._expire(channel, time))
