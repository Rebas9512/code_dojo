def choose_pairs(nums: list[int]) -> list[list[int]]:
    values = sorted(nums)
    result, path = [], []
    def visit(start):
        if len(path) == 2:
            result.append(path[:])
            return
        for i in range(start, len(values)):
            if i > 0 and values[i] == values[i - 1]:
                continue
            path.append(values[i])
            visit(i + 1)
            path.pop()
    visit(0)
    return result


def run_case(nums: list[int]) -> list[list[int]]:
    # 组合的成员可以任意排列；保留每一项和全部重复次数。
    return [sorted(group) for group in choose_pairs(nums)]
