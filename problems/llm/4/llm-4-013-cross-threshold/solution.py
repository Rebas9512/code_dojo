mass, kept = 0.0, []
for i, prob in enumerate([0.5, 0.25, 0.25]):
    kept.append(i)
    mass += prob
    if mass >= 0.75:
        break
print(kept)
