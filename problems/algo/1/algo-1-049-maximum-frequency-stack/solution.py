from collections import defaultdict


class FreqStack:
    def __init__(self):
        self.counts = defaultdict(int)
        self.levels = defaultdict(list)
        self.highest = 0

    def push(self, val: int) -> None:
        self.counts[val] += 1
        level = self.counts[val]
        self.levels[level].append(val)
        self.highest = max(self.highest, level)

    def pop(self) -> int:
        level = self.levels[self.highest]
        val = level.pop()
        self.counts[val] -= 1
        if not level:
            self.highest -= 1
        return val
