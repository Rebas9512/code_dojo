def check(args, expected, actual):
    nums = args[0]
    return (
        type(actual) is int
        and 0 <= actual < len(nums)
        and (actual == 0 or nums[actual] > nums[actual - 1])
        and (actual == len(nums) - 1 or nums[actual] > nums[actual + 1])
    )
