def check(args, expected, actual):
    if not isinstance(actual, list) or any(v is not None and type(v) is not int for v in actual):
        return False
    target = sorted(v for v in expected if v is not None)
    if not actual:
        return not target
    # 每个非空孩子继承祖先划出的上下界，同时记录父子下标。
    pending = [(0, None, None)]
    children = {}
    head, pos = 0, 1
    while head < len(pending):
        index, low, high = pending[head]
        head += 1
        value = actual[index]
        if value is None or (low is not None and value <= low) or (high is not None and value >= high):
            return False
        children[index] = []
        for lo, hi in ((low, value), (value, high)):
            if pos < len(actual) and actual[pos] is not None:
                pending.append((pos, lo, hi))
                children[index].append(pos)
            pos += 1
    if pos < len(actual) or sorted(actual[i] for i in children) != target:
        return False
    heights = {}
    for index in reversed(children):
        sizes = [heights[c] for c in children[index]] + [0, 0]
        if abs(sizes[0] - sizes[1]) > 1:
            return False
        heights[index] = max(sizes) + 1
    return True
