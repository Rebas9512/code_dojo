class Counter:
    def __init__(self, start: int):
        self.value = start

    def add(self, step: int) -> None:
        self.value += step

    def get(self) -> int:
        return self.value
