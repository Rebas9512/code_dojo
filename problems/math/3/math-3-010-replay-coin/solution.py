from random import seed, randint

seed(7)
flips = [randint(0, 1) for i in range(3)]
print(flips == [1, 0, 1])
print(sum(flips))
