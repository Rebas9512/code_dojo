def alien_order(words: list[str]) -> str:
    degree = {ch: 0 for word in words for ch in word}
    after = {ch: set() for ch in degree}
    for i in range(1, len(words)):
        first, second = words[i - 1], words[i]
        for a, b in zip(first, second):
            if a != b:
                if b not in after[a]:
                    after[a].add(b)
                    degree[b] += 1
                break
        else:
            if len(first) > len(second):
                return ""
    ready = [ch for ch in degree if degree[ch] == 0]
    order = []
    while ready:
        ch = ready.pop()
        order.append(ch)
        for nxt in after[ch]:
            degree[nxt] -= 1
            if degree[nxt] == 0:
                ready.append(nxt)
    return "".join(order) if len(order) == len(degree) else ""
