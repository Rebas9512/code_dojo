class StockSpanner:
    def __init__(self):
        self.stack = []

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            _, days = self.stack.pop()
            span += days
        self.stack.append((price, span))
        return span
