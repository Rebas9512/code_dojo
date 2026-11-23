def can_fill(values, k):
    total = sum(values)
    side = total // k
    if total % k or max(values) > side or len(values) < k:
        return False
    sticks = sorted(values, reverse=True)
    loads = [0] * k
    def place(index):
        if index == len(sticks):
            return True
        tried = set()
        for j, load in enumerate(loads):
            if load in tried or load + sticks[index] > side:
                continue
            tried.add(load)
            loads[j] += sticks[index]
            if place(index + 1):
                return True
            loads[j] -= sticks[index]
        return False
    return place(0)

def makes_square(sticks: list[int]) -> bool:
    return can_fill(sticks, 4)
