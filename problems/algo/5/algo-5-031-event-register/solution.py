class EventCounter:
    def __init__(self):
        self.total = 0

    def hit(self, time: int) -> None:
        self.total += 1

    def count(self, time: int) -> int:
        return self.total
