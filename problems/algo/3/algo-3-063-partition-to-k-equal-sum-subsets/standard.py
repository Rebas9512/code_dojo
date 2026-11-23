def equal_groups(nums: list[int], k: int) -> bool:
    total = sum(nums)
    target = total // k
    if total % k or max(nums) > target:
        return False
    values = sorted(nums, reverse=True)
    sums = [0] * k

    def place(index):
        if index == len(values):
            return True
        value = values[index]
        tried = set()
        for bag, current in enumerate(sums):
            if current in tried or current + value > target:
                continue
            tried.add(current)
            sums[bag] += value
            if place(index + 1):
                return True
            sums[bag] -= value
        return False

    return place(0)
