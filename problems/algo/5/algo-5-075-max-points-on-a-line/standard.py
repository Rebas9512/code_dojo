import math


def most_points(points: list[list[int]]) -> int:
    best = 1
    for i, (x, y) in enumerate(points):
        slopes = {}
        for j in range(i + 1, len(points)):
            other_x, other_y = points[j]
            dx, dy = other_x - x, other_y - y
            factor = math.gcd(dx, dy)
            dx, dy = dx // factor, dy // factor
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            key = (dx, dy)
            slopes[key] = slopes.get(key, 0) + 1
            best = max(best, 1 + slopes[key])
    return best
