counts = {(4, 0): 2, (1, 9): 2, (0, 0): 1}
print(min(counts, key=lambda pair: (-counts[pair], pair)))
