def breaks(groups: list[list[list[int]]]) -> list[list[int]]:
    spans = sorted(span for group in groups for span in group)
    end = spans[0][1]
    out = []
    for left, right in spans:
        if left > end:
            out.append([end, left])
        end = max(end, right)
    return out
