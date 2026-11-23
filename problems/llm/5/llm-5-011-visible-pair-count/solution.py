def visible_pairs(prompt_len, steps):
    full = 0
    cached = 0
    for i in range(steps):
        length = prompt_len + i
        triangle = length * (length + 1) // 2
        full += triangle
        cached += triangle if i == 0 else length
    return [full, cached]
