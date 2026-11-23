def search_grid(matrix: list[list[int]], target: int) -> bool:
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols
    while lo < hi:
        mid = (lo + hi) // 2
        if matrix[mid // cols][mid % cols] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo < rows * cols and matrix[lo // cols][lo % cols] == target
