class Groups:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def root(self, node):
        while node != self.parent[node]:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def merge_sets(self, a, b):
        a, b = self.root(a), self.root(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True

def redundant(edges: list[list[int]]) -> list[int]:
    groups = Groups(len(edges) + 1)
    for a, b in edges:
        if not groups.merge_sets(a, b):
            return [a, b]
