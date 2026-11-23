counts = {}
for name in ["林", "苏", "林"]:
    if name not in counts:
        print("建格")
        counts[name] = 0
    counts[name] += 1
    print(counts[name])
