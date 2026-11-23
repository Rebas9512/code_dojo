def subset_xor_sum(nums: list[int]) -> int:
    def visit(i, value):
        if i == len(nums):
            return value
        return visit(i + 1, value) + visit(i + 1, value ^ nums[i])
    return visit(0, 0)
