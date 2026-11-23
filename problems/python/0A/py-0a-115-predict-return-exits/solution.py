def size(n):
    if n > 10:
        return "大"
    if n > 5:
        return "中"
    return "小"

print(size(20))
print(size(7))
print(size(10))
print(size(3))
