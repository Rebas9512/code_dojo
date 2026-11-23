words = ["pen", "ink", "pad"]
by_initial = {w[0]: w for w in words}
letters = {w[0] for w in words}
print(by_initial["p"])
print(len(letters))
