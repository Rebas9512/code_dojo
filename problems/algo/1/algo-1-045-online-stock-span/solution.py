class StockSpanner:
    def __init__(self):
        self.stack = []

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            old_price, days = self.stack.pop()
            span += days
        self.stack.append((price, span))
        return span
