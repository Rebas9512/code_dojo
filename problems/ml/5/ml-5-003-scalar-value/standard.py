from math import tanh


class Value:
    def __init__(self, data, parents=()):
        self.data = float(data)
        self.grad = 0.0
        self.parents = parents

    def __add__(self, other):
        return Value(self.data + other.data, ((self, 1.0), (other, 1.0)))

    def __mul__(self, other):
        return Value(self.data * other.data, ((self, other.data), (other, self.data)))

    def tanh(self):
        result = tanh(self.data)
        return Value(result, ((self, 1 - result**2),))


def make_value(x):
    return Value(x)
