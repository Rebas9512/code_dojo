def gcd_connected(nums: list[int]) -> bool:
    if len(nums) == 1:
        return True
    if 1 in nums:
        return False
    limit = max(nums)
    # 用筛法登记每个数的最小质因子，随后可以连续整除分解。
    factor = list(range(limit + 1))
    for prime in range(2, int(limit ** 0.5) + 1):
        if factor[prime] == prime:
            for multiple in range(prime * prime, limit + 1, prime):
                if factor[multiple] == multiple:
                    factor[multiple] = prime
    parent = list(range(len(nums)))

    def root(i):
        while i != parent[i]:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    owner = {}
    for i, value in enumerate(nums):
        while value > 1:
            prime = factor[value]
            if prime in owner:
                parent[root(i)] = root(owner[prime])
            else:
                owner[prime] = i
            while value % prime == 0:
                value //= prime
    return all(root(i) == root(0) for i in range(len(nums)))
