counts = {}
for name in ["Lin", "Su", "Lin"]:
    if name not in counts:
        print("new entry")
        counts[name] = 0
    counts[name] += 1
    print(counts[name])
