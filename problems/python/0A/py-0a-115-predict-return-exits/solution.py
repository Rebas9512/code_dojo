def size(n):
    if n > 10:
        return "large"
    if n > 5:
        return "medium"
    return "small"

print(size(20))
print(size(7))
print(size(10))
print(size(3))
