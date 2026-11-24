def block(x, norm1, attention, norm2, mlp):
    middle = x + attention(norm1(x))
    return middle + mlp(norm2(middle))
