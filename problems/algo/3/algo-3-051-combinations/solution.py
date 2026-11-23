def choose(n: int, k: int) -> list[list[int]]:
    result, path = [], []
    def fill(start):
        if len(path) == k:
            result.append(path[:])
            return
        missing = k - len(path)
        for number in range(start, n - missing + 2):
            path.append(number)
            fill(number + 1)
            path.pop()
    fill(1)
    return result


def run_case(n: int, k: int) -> list[list[int]]:
    # 组合的成员可以任意排列；保留每一项和全部重复次数。
    return [sorted(group) for group in choose(n, k)]
