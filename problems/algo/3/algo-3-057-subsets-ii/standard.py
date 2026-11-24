def subsets(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    answers, path = [], []

    def visit(start):
        answers.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            visit(i + 1)
            path.pop()

    visit(0)
    return answers


def run_case(nums: list[int]) -> list[list[int]]:
    # 组合的成员可以任意排列；保留每一项和全部重复次数。
    return [sorted(group) for group in subsets(nums)]
