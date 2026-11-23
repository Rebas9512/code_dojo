def merge(a: list[int], b: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    return result + a[i:] + b[j:]


def sort_array(nums: list[int]) -> list[int]:
    if len(nums) < 2:
        return nums
    mid = len(nums) // 2
    return merge(sort_array(nums[:mid]), sort_array(nums[mid:]))
