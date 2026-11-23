def ending_sums(nums: list[int]) -> list[int]:
    ending = nums[0]
    record = [ending]
    for value in nums[1:]:
        ending = max(value, ending + value)
        record.append(ending)
    return record
