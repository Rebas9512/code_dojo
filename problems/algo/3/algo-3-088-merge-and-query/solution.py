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

def connectivity(n: int, operations: list[list]) -> list[bool]:
    groups = Groups(n)
    answers = []
    for kind, a, b in operations:
        if kind == 'join':
            groups.merge_sets(a, b)
        else:
            answers.append(groups.root(a) == groups.root(b))
    return answers
