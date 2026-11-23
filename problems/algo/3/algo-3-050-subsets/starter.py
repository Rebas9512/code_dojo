def subsets(nums: list[int]) -> list[list[int]]:
    pass

def run_case(nums: list[int]) -> list[list[int]]:
    # 组合的成员可以任意排列；保留每一项和全部重复次数。
    return [sorted(group) for group in subsets(nums)]
