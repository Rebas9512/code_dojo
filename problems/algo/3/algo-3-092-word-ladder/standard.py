from collections import deque


def ladder_length(begin: str, end: str, words: list[str]) -> int:
    remaining = set(words)
    if end not in remaining:
        return 0
    remaining.discard(begin)
    queue = deque([(begin, 1)])
    while queue:
        word, length = queue.popleft()
        for i in range(len(word)):
            prefix = word[:i]
            suffix = word[i + 1 :]
            for ch in 'abcdefghijklmnopqrstuvwxyz':
                other = prefix + ch + suffix
                if other == end:
                    return length + 1
                if other in remaining:
                    remaining.remove(other)
                    queue.append((other, length + 1))
    return 0
