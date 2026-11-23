def count_queens(n: int) -> int:
    columns = set()
    down = set()
    up = set()

    def place(row):
        if row == n:
            return 1
        count = 0
        for col in range(n):
            diagonal = row - col
            other_diagonal = row + col
            if col not in columns and diagonal not in down and other_diagonal not in up:
                columns.add(col)
                down.add(diagonal)
                up.add(other_diagonal)
                count += place(row + 1)
                columns.remove(col)
                down.remove(diagonal)
                up.remove(other_diagonal)
        return count

    return place(0)
