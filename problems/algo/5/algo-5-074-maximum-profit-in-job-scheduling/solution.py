import bisect


def earn(start: list[int], end: list[int], pay: list[int]) -> int:
    jobs = sorted(zip(end, start, pay))
    ends = []
    best = [0]
    for finish, begin, fee in jobs:
        count = bisect.bisect_right(ends, begin)
        best.append(max(best[-1], best[count] + fee))
        ends.append(finish)
    return best[-1]
