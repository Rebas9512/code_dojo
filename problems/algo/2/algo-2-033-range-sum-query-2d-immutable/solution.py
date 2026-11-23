class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        rows, cols = len(matrix), len(matrix[0])
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            row_sum = 0
            for c in range(cols):
                row_sum += matrix[r][c]
                self.prefix[r + 1][c + 1] = self.prefix[r][c + 1] + row_sum

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        p = self.prefix
        return (p[row2 + 1][col2 + 1] - p[row1][col2 + 1]
                - p[row2 + 1][col1] + p[row1][col1])
