def intersection(a: list[int], b: list[int]) -> list[int]:
    i = j = 0
    pairs = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif a[i] > b[j]:
            j += 1
        else:
            pairs.append(a[i])
            i += 1
            j += 1
    return pairs
