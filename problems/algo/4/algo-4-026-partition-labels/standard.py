def partition_sizes(s: str) -> list[int]:
    last = {letter: i for i, letter in enumerate(s)}
    start = end = 0
    sizes = []
    for i, letter in enumerate(s):
        end = max(end, last[letter])
        if i == end:
            sizes.append(end - start + 1)
            start = i + 1
    return sizes
