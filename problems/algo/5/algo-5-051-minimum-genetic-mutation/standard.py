from collections import deque


def mutations(start: str, end: str, bank: list[str]) -> int:
    allowed = set(bank)
    queue = deque([(start, 0)])
    allowed.discard(start)
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(8):
            for ch in "ACGT":
                other = word[:i] + ch + word[i + 1 :]
                if other in allowed:
                    allowed.remove(other)
                    queue.append((other, steps + 1))
    return -1
