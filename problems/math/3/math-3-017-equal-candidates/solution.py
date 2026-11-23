from math import exp

scores = [1200, 1200]
w = [exp(s-max(scores)) for s in scores]
print([v/sum(w) for v in w])
