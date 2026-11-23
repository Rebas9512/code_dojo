def trapped_water(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_wall, right_wall = height[left], height[right]
    total = 0
    while left < right:
        if left_wall <= right_wall:
            left += 1
            left_wall = max(left_wall, height[left])
            total += left_wall - height[left]
        else:
            right -= 1
            right_wall = max(right_wall, height[right])
            total += right_wall - height[right]
    return total
