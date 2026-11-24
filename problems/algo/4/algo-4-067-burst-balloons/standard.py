def burst_score(nums: list[int]) -> int:
    # 两个哨兵始终保留，枚举开区间内最后消失的气球。
    values = [1] + nums + [1]
    n = len(values)
    best = [[0] * n for _ in range(n)]
    for gap in range(2, n):
        for left in range(n - gap):
            right = left + gap
            sides = values[left] * values[right]
            for last in range(left + 1, right):
                score = best[left][last] + sides * values[last] + best[last][right]
                best[left][right] = max(best[left][right], score)
    return best[0][-1]
