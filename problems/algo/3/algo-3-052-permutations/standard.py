def arrangements(nums: list[int]) -> list[list[int]]:
    result, path = [], []
    used = [False] * len(nums)

    def fill():
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i, value in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(value)
            fill()
            path.pop()
            used[i] = False

    fill()
    return result
