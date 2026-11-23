class TinySet:
    def __init__(self):
        self.values = []

    def contains(self, x: int) -> bool:
        return x in self.values

    def add(self, x: int) -> None:
        if not self.contains(x):
            self.values.append(x)
