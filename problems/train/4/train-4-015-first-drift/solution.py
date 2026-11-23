ref = [4., 2., 1., 0.5]
run = [4., 2.125, 1.5, 0.5]
print([i + 1 for i in range(len(ref)) if abs(ref[i] - run[i]) > 0.125])
