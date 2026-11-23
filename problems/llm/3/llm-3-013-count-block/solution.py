c = 8
attention = 4 * c * c
mlp = c * (2 * c) + (2 * c) * c
norms = 2 * (c + c)
print(attention + mlp + norms)
