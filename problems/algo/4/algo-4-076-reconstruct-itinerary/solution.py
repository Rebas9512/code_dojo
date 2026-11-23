def itinerary(tickets: list[list[str]]) -> list[str]:
    outgoing = {}
    for src, dst in sorted(tickets, reverse=True):
        outgoing.setdefault(src, []).append(dst)
    stack = ["JFK"]
    # 没票可走的地点是当前子行程的尾端，回退时才写入答案。
    reverse_route = []
    while stack:
        node = stack[-1]
        if outgoing.get(node):
            stack.append(outgoing[node].pop())
        else:
            reverse_route.append(stack.pop())
    return reverse_route[::-1]
