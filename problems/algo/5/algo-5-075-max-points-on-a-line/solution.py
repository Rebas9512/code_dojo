import math


def most_points(points: list[list[int]]) -> int:
    best = 1
    for i, (x, y) in enumerate(points):
        slopes = {}
        for xx, yy in points[i + 1 :]:
            dx, dy = xx - x, yy - y
            factor = math.gcd(dx, dy)
            dx, dy = dx // factor, dy // factor
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            key = (dx, dy)
            slopes[key] = slopes.get(key, 0) + 1
            best = max(best, 1 + slopes[key])
    return best
