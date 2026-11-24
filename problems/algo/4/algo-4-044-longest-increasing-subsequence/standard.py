import bisect


def lis_length(nums: list[int]) -> int:
    # tails[i] 保存长度 i+1 的递增子序列能达到的最小末尾。
    tails = []
    for value in nums:
        i = bisect.bisect_left(tails, value)
        if i == len(tails):
            tails.append(value)
        else:
            tails[i] = value
    return len(tails)
