def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    for index in range(i, len(a)):
        result.append(a[index])
    for index in range(j, len(b)):
        result.append(b[index])
    return result
