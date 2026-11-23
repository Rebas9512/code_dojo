class Stack:
    def __init__(self):
        self.pages = []

    def push(self, x: int) -> None:
        self.pages.append(x)

    def pop(self) -> int | None:
        if self.pages:
            return self.pages.pop()
        return None

    def peek(self) -> int | None:
        if self.pages:
            return self.pages[-1]
        return None

    def size(self) -> int:
        return len(self.pages)
