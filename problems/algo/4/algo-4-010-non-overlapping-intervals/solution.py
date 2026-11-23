def erase_overlaps(intervals: list[list[int]]) -> int:
    end = None
    removed = 0
    for start, stop in sorted(intervals, key=lambda span: span[1]):
        if end is None or start >= end:
            end = stop
        else:
            removed += 1
    return removed
