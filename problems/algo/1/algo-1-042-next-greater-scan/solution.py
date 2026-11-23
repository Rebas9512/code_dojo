def next_greater(nums: list[int]) -> list[int]:
    answer = [-1] * len(nums)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[j] > nums[i]:
                answer[i] = nums[j]
                break
    return answer
