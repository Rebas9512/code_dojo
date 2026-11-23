def pal_pairs(words: list[str]) -> list[list[int]]:
    def pal_prefixes(word):
        # 原串与逆串拼接后，同时是前缀和后缀的片段恰为回文前缀。
        text = word + "#" + word[::-1]
        border = [0] * len(text)
        for i in range(1, len(text)):
            j = border[i - 1]
            while j and text[i] != text[j]:
                j = border[j - 1]
            if text[i] == text[j]:
                j += 1
            border[i] = j
        sizes = {0}
        j = border[-1]
        while j:
            sizes.add(j)
            j = border[j - 1]
        return sizes

    # 每个节点存出边、恰好结束的词号与剩余前缀成回文的词号。
    root = [{}, -1, []]
    for i, word in enumerate(words):
        prefixes = pal_prefixes(word)
        node = root
        for pos in range(len(word) - 1, -1, -1):
            if pos + 1 in prefixes:
                node[2].append(i)
            ch = word[pos]
            if ch not in node[0]:
                node[0][ch] = [{}, -1, []]
            node = node[0][ch]
        node[1] = i
        node[2].append(i)

    out = []
    for i, word in enumerate(words):
        suffix_sizes = pal_prefixes(word[::-1])
        node = root
        for pos, ch in enumerate(word):
            end = node[1]
            if end >= 0 and end != i and len(word) - pos in suffix_sizes:
                out.append([i, end])
            node = node[0].get(ch)
            if node is None:
                break
        if node is not None:
            out.extend([i, j] for j in node[2] if j != i)
    return out
