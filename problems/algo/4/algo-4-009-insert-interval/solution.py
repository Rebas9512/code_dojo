def insert_span(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    result = []
    start, end = new
    i = 0
    while i < len(intervals) and intervals[i][1] < start:
        result.append(intervals[i])
        i += 1
    while i < len(intervals) and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])
    return result + intervals[i:]
