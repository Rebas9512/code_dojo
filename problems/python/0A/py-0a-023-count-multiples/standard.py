def count_multiples(n: int) -> int:
    count = 0
    for i in range(1, n + 1):
        if i % 3 == 0 or i % 5 == 0:
            count += 1
    return count
