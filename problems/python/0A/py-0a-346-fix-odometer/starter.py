class Meter:
    def __init__(self, start: int):
        self.distance = start

    def advance(self, k: int) -> int:
        distance = self.distance + k
        return distance

    def read(self) -> int:
        return self.distance
