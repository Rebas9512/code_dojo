def four_sum(nums: list[int], target: int) -> list[list[int]]:
    values = sorted(nums)
    result = []
    for i in range(len(values) - 3):
        if i > 0 and values[i] == values[i - 1]:
            continue
        for j in range(i + 1, len(values) - 2):
            if j > i + 1 and values[j] == values[j - 1]:
                continue
            left, right = j + 1, len(values) - 1
            while left < right:
                total = values[i] + values[j] + values[left] + values[right]
                if total < target:
                    left += 1
                elif total > target:
                    right -= 1
                else:
                    result.append([values[i], values[j], values[left], values[right]])
                    left += 1
                    right -= 1
                    while left < right and values[left] == values[left - 1]:
                        left += 1
    return result
