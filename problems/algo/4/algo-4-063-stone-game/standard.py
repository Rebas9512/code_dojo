def first_wins(piles: list[int]) -> bool:
    lead = piles[:]
    for length in range(2, len(piles) + 1):
        for left in range(len(piles) - length + 1):
            right = left + length - 1
            lead[left] = max(piles[left] - lead[left + 1], piles[right] - lead[left])
    return lead[0] > 0
