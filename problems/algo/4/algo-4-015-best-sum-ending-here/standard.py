def ending_sums(nums: list[int]) -> list[int]:
    ending = nums[0]
    record = [ending]
    for i in range(1, len(nums)):
        value = nums[i]
        ending = max(value, ending + value)
        record.append(ending)
    return record
