class DetectSquares:
    def __init__(self):
        self.columns = {}

    def add(self, point: list[int]) -> None:
        x, y = point
        column = self.columns.setdefault(x, {})
        column[y] = column.get(y, 0) + 1

    def count(self, point: list[int]) -> int:
        x, y = point
        total = 0
        for other_y, copies in self.columns.get(x, {}).items():
            side = other_y - y
            if side == 0:
                continue
            for other_x in (x - side, x + side):
                column = self.columns.get(other_x, {})
                total += copies * column.get(y, 0) * column.get(other_y, 0)
        return total
