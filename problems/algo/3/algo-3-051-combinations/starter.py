def choose(n: int, k: int) -> list[list[int]]:
    pass

def run_case(n: int, k: int) -> list[list[int]]:
    # 组合的成员可以任意排列；保留每一项和全部重复次数。
    return [sorted(group) for group in choose(n, k)]
