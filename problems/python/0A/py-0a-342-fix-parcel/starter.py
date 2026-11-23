class Parcel:
    def __init__(self, net: int, tare: int):
        weight = net + tare


def weigh(net: int, tare: int) -> int:
    parcel = Parcel(net, tare)
    return parcel.weight
