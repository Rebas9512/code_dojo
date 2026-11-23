from collections import defaultdict, OrderedDict


class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.values = {}
        self.frequency = {}
        self.levels = defaultdict(OrderedDict)
        self.lowest = 0

    def _touch(self, key):
        old = self.frequency[key]
        del self.levels[old][key]
        if not self.levels[old]:
            del self.levels[old]
            if self.lowest == old:
                self.lowest = old + 1
        self.frequency[key] = old + 1
        self.levels[old + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.values:
            return -1
        self._touch(key)
        return self.values[key]

    def put(self, key: int, value: int) -> None:
        if key in self.values:
            self.values[key] = value
            self._touch(key)
            return
        if len(self.values) == self.capacity:
            group = self.levels[self.lowest]
            victim, _ = group.popitem(last=False)
            if not group:
                del self.levels[self.lowest]
            del self.frequency[victim]
            del self.values[victim]
        self.values[key] = value
        self.frequency[key] = self.lowest = 1
        self.levels[1][key] = None
