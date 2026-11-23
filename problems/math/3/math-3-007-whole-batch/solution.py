xs = [1, 5]
m = sum(xs) / len(xs)
print(sum((x-m)**2 for x in xs) / len(xs))
