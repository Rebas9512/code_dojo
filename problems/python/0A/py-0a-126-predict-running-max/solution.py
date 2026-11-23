n = 1938
best = n % 10
while n > 0:
    digit = n % 10
    if digit > best:
        best = digit
    print(digit, best)
    n = n // 10
print("max", best)
