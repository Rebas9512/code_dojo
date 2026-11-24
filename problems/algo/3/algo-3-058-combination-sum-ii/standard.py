def sum_choices(nums: list[int], target: int) -> list[list[int]]:
    values = sorted(nums)
    result, path = [], []

    def visit(start, left):
        if left == 0:
            result.append(path[:])
            return
        for i in range(start, len(values)):
            value = values[i]
            if i > start and value == values[i - 1]:
                continue
            if value > left:
                break
            path.append(value)
            visit(i + 1, left - value)
            path.pop()

    visit(0, target)
    return result


def run_case(nums: list[int], target: int) -> list[list[int]]:
    # 组合的成员可以任意排列；保留每一项和全部重复次数。
    return [sorted(group) for group in sum_choices(nums, target)]
