from collections import deque


def open_lock(deadends: list[str], target: str) -> int:
    seen = set(deadends)
    if '0000' in seen:
        return -1
    queue = deque([('0000', 0)])
    seen.add('0000')
    while queue:
        code, turns = queue.popleft()
        if code == target:
            return turns
        for i, digit in enumerate(code):
            for step in (-1, 1):
                new = code[:i] + str((int(digit) + step) % 10) + code[i+1:]
                if new not in seen:
                    seen.add(new)
                    queue.append((new, turns + 1))
    return -1
