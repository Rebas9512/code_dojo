def makes_square(sticks: list[int]) -> bool:
    total = sum(sticks)
    side = total // 4
    if total % 4 or max(sticks) > side:
        return False
    lengths = sorted(sticks, reverse=True)
    sides = [0] * 4

    def place(index):
        if index == len(lengths):
            return True
        length = lengths[index]
        tried = set()
        for edge, used in enumerate(sides):
            if used in tried or used + length > side:
                continue
            tried.add(used)
            sides[edge] += length
            if place(index + 1):
                return True
            sides[edge] -= length
        return False

    return place(0)
