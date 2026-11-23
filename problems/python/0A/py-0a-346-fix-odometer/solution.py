class Meter:
    def __init__(self, start: int):
        self.distance = start

    def advance(self, k: int) -> int:
        self.distance = self.distance + k
        return self.distance

    def read(self) -> int:
        return self.distance
