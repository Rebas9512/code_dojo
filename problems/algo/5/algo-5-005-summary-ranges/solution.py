def ranges(nums: list[int]) -> list[str]:
    out = []
    i = 0
    while i < len(nums):
        first = nums[i]
        while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
            i += 1
        last = nums[i]
        out.append(str(first) if first == last else f"{first}->{last}")
        i += 1
    return out
