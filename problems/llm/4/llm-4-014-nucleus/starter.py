def nucleus(probs, p):
    order = sorted(range(len(probs)), key=lambda i: (-probs[i], i))
    mass = 0.0
    kept = []
    for i in order:
        kept.append(i)
        mass += probs[i]
        if ...:
            break
    return kept
