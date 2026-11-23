def min_extra(text: str, words: list[str]) -> int:
    root = {}
    for word in words:
        node = root
        for letter in word:
            node = node.setdefault(letter, {})
        node["#"] = True
    # 一层允许多跳过一个字符。层内先走完所有免费的整词。
    frontier = {0}
    seen = set()
    for skipped in range(len(text) + 1):
        stack = list(frontier)
        frontier = set()
        while stack:
            start = stack.pop()
            if start == len(text):
                return skipped
            if start in seen:
                continue
            seen.add(start)
            frontier.add(start + 1)
            node = root
            for end in range(start, len(text)):
                if text[end] not in node:
                    break
                node = node[text[end]]
                if "#" in node:
                    stack.append(end + 1)
