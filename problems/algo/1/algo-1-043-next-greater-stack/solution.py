def next_greater(nums: list[int]) -> list[int]:
    answer = [-1] * len(nums)
    pending = []
    for i, value in enumerate(nums):
        while pending and nums[pending[-1]] < value:
            previous = pending.pop()
            answer[previous] = value
        pending.append(i)
    return answer
