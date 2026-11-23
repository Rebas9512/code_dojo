from collections import defaultdict, deque


def buses(routes: list[list[int]], source: int, target: int) -> int:
    if source == target:
        return 0
    lines = defaultdict(list)
    for i, stops in enumerate(routes):
        for stop in stops:
            lines[stop].append(i)
    queue = deque([(source, 0)])
    used = set()
    while queue:
        stop, count = queue.popleft()
        for line in lines.pop(stop, []):
            if line in used:
                continue
            used.add(line)
            for other in routes[line]:
                if other == target:
                    return count + 1
                queue.append((other, count + 1))
    return -1
