length, steps = 2, 4
full = sum(range(length, length + steps))
cached = length + steps - 1
print(full, cached, full - cached)
