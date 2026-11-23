def first_repeat(nums: list[int]) -> int | None:
    seen = set()
    for value in nums:
        if value in seen:
            return value
        ____  # 把本轮读数记下来
    return None
