def classify_edges(n: int, edges: list[list[int]]) -> list[list[int]]:
    ranked = sorted(range(len(edges)), key=lambda i: edges[i][2])

    def tree_cost(skip=-1, force=-1):
        parent = list(range(n))

        def root(node):
            while node != parent[node]:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        cost = used = 0
        if force >= 0:
            u, v, cost = edges[force]
            parent[u] = v
            used = 1
        for i in ranked:
            if i == skip or i == force:
                continue
            u, v, weight = edges[i]
            a, b = root(u), root(v)
            if a != b:
                parent[a] = b
                cost += weight
                used += 1
        return cost if used == n - 1 else float("inf")

    # 先禁用、再强制一条边，两次结果都和原最低总价比较。
    minimum = tree_cost()
    must, may = [], []
    for i in ranked:
        if tree_cost(skip=i) > minimum:
            must.append(i)
        elif tree_cost(force=i) == minimum:
            may.append(i)
    return [must, may]
