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


def merge_accounts(accounts: list[list[str]]) -> list[list[str]]:
    groups = Groups(len(accounts))
    owner = {}
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in owner:
                groups.merge_sets(i, owner[email])
            else:
                owner[email] = i
    merged = {}
    for email, i in owner.items():
        merged.setdefault(groups.root(i), []).append(email)
    return [[accounts[i][0]] + sorted(emails) for i, emails in merged.items()]
